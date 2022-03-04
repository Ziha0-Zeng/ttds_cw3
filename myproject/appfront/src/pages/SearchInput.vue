<template>
    <div>
        <div class="icon_box">
            <img src="../assets/logo.png">
        </div>
        <div class = "search_box">
            <img src="../assets/search.png">
            <input type="text" name = "query" placeholder="Search for a paper here" v-model="query">
            <button @click="send_query(query)">search</button >
            <div class="advancedSearch">
                <AdvancedSearch></AdvancedSearch>
            </div>
        </div>
    </div>
</template>

<script>

import AdvancedSearch from '../components/AdvanceSearch'
export default {
    name: 'SearchInput',
    components:{AdvancedSearch},
    data(){
        return {
            query:""
		}
    },
    methods: {
		send_query(q){
            if(this.query.length > 0){
                this.$router.push ({
                    name: 'searchPage',
                    query:{
                        query:q
                    }
                })
            }
		}
	}
    
}
</script>

<style scoped>
.icon_box{
    text-align: center;
    margin-top: 200px;
    margin-bottom: 30px;
}

.search_box{
    position: relative;
    width: 550px;
    height: 40px;
    margin: auto;

}
.search_box img{
    position: absolute;
    vertical-align: center;
    top: 15px;
    left: 15px;
    height: 15px;
}

.search_box input{
    width: 100% ;
    height: 40px;
    border-width: 1px;
    border-style: solid;
    border-radius: 30px;
    border-color: gainsboro;
    font-size: 16px;
    padding-left: 40px;
}

.search_box input:HOVER{
    -webkit-transition:-webkit-box-shadow linear .2s;
    -webkit-box-shadow:0 0 18px rgba(210,210,210,3);
}

.search_box input:focus{
    outline: none;
}
.search_box button{
    position: absolute;
    top: 0px;
    right: -49px;
    height: 44px;
    border: none;
    background-color: rgb(78, 110, 242);
    color: white;
    border-radius:30px;
    outline: none;
    width: 100px;
    font-size: 20px;
    padding: 5px;

}
.search_box button:HOVER{
    background-color: #2b56f0;
}

.advancedSearch{
    margin-top:40px;
}
</style>