<template>
    <div class = "filterBox">
        <el-col style="width: 200px">
            <el-menu
            default-active="1-1"
            class="el-menu-vertical-demo"
            background-color="#fff"
            text-color="#000"
            active-text-color="#ffd04b" style="height:auto">

            <el-menu-item-group>
                <template slot="title">Time Filter</template>
                <el-menu-item index="1-1" @click="timeFilter(0)">No limitation</el-menu-item>
                <el-menu-item index="1-2" @click="timeFilter(1)">Since 2022</el-menu-item>
                <el-menu-item index="1-3" @click="timeFilter(2)">Since 2021</el-menu-item>
                <el-menu-item index="1-4" @click="timeFilter(3)">Since 2018</el-menu-item>
            </el-menu-item-group>
            </el-menu>
        </el-col>
        <el-col style="width: 200px">
            <el-menu
            default-active="1-1"
            class="el-menu-vertical-demo"
            background-color="#fff"
            text-color="#000"
            active-text-color="#ffd04b" 
            style="height:auto">

            <el-menu-item-group>
                <template slot="title">Rank</template>
                <el-menu-item index="1-1" @click="rankSort(0)">Sort by Relevance</el-menu-item>
                <el-menu-item index="1-2" @click="rankSort(1)">Sort by Date</el-menu-item>
            </el-menu-item-group>
            </el-menu>
        </el-col>
    </div>
    

</template>

<script>

export default {
    name: 'FilterElement',

    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        timeFilter(filterVal){
            console.log("time filter " + filterVal);
            this.$bus.$emit('filter', filterVal);
        },
        rankSort(rankVal){
            console.log("rankSort " + rankVal);
            this.$bus.$emit('rank', rankVal);

        }
    }

}
</script>

<style>
.filterBox{
    position: relative;
    left: 40px;
    width: 200px;
    height: 100%;
    float: left;
}

</style>