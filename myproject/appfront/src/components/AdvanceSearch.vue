<template>
    <div>
        <div>
            <el-switch
            :width='40'
            v-model="value"
            active-color="#5773ff"
            inactive-color="#f2f2f2"
            active-text="Advanced Search"
            class = "advanceSearchBtn">
            </el-switch>
        </div>
        
        <div>
            <el-form ref="myForm" :model="sizeForm" size="mini" v-show="value" style="width:600px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="Keywords">
                            <el-input v-model="sizeForm.keywords" placeholder="Keywords in paper" style="width:200px"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="Authors">
                            <el-input v-model="sizeForm.authors" placeholder="Authors" style="width:200px"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="20">
                        <el-form-item label="Date">
                            <el-date-picker
                                v-model="sizeForm.dateRange"
                                type="daterange"
                                range-separator="to"
                                start-placeholder="Start Date"
                                end-placeholder="End Date"
                                style="width:300px"
                                format="yyyy-MM-dd"
                                value-format="yyyy-MM-dd"
                            >
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    
                </el-row>
                
                <el-form-item size="large">
                    <el-button type="primary" icon="el-icon-search" @click="onSubmit" style="width:100px">Search</el-button>
                    <el-button type="warning" @click="resetForm" icon="el-icon-refresh-right" plain style="width:100px">Reset</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    export default {
        name:'AdvancedSearch',
        data() {
            return {
                sizeForm: {
                    authors: '',
                    keywords: '',
                    startDate: '',
                    endDate:'',
                    dateRange:'',
                },
                value: false,
                startTime: {

                    disabledDate: time => {
                        let endDateVal = this.sizeForm.endDate;
                        console.log("start" + this.sizeForm.endDate);
                        if (endDateVal!="") {
                            return time.getTime() > new Date(endDateVal).getTime();
                        }
                    }
                },
                endTime: {
                    disabledDate: time => {
                        let startDateVal = this.sizeForm.startDate;
                        console.log("end"+this.sizeForm.startDate);
                        if (startDateVal!="") {
                            return time.getTime() < new Date(startDateVal).getTime();
                        }
                    }
                }
            };
        },
        methods: {
            onSubmit() {
                console.log('submit!');
                if(this.sizeForm.keywords.length > 0){
                    this.$router.push ({
                        name: 'searchPage',
                        query:{
                            query:this.sizeForm.keywords,
                            authors:this.sizeForm.authors,
                            startDate:this.sizeForm.startDate,
                            endDate:this.sizeForm.endDate
                        }
                    })

                    // submit the query
                    axios.get(
                        `http://localhost:8000/myapp/advancedSearch/?keyword=${this.sizeForm.keywords}&authors=${this.sizeForm.authors}&startDate=${this.sizeForm.startDate}&endDate=${this.sizeForm.endDate}`
                        ).then(
                        response => {
                            console.log("success", response.data);
                            this.$bus.$emit('getUsers', response.data);
                        },
                        error => { 
                            console.log("fail", error.message);
                        }
                    )
                }

            },
            resetForm(){
                this.sizeForm.authors='';
                this.sizeForm.keywords='';
                this.sizeForm.startDate='';
                this.sizeForm.endDate='';
            },

        },

        watch:{
            "sizeForm.dateRange": function(newVal){
                this.sizeForm.startDate=newVal[0]
                this.sizeForm.endDate=newVal[1]
            }
        }
    };
</script>

<style scoped>
.advanceSearchBtn{
    padding-top: 10px;
    padding-bottom: 15px;
}
</style>
