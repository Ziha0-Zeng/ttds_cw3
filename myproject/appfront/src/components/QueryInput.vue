<template>
    <div class= "outer_box">
        <div class="icon_box">
            <img src = "../assets/logo.png" class = "logo_img">
        </div>
        <div class = "search_box">
            <img src="../assets/search.png" class="search_img">
            <input type="text" name = "query" v-model="query">
            <button @click="send_query()"> Search </button>
            
        </div>
    </div>
    
</template>

<script>
import axios from 'axios'
export default {
    name:'QueryInput',
    data(){
        return {
            query:"",
		}
    },
    methods: {
		send_query(){
            if(this.query.length > 0){
                // submit the query
                // this.$router.push ({
                //     name: 'searchPage',
                //     query:{
                //         query:this.query,
                //     }
                // })
                // axios.get(`https://api.github.com/search/users?q=${this.query}`).then(
                //     response => {
                //         console.log("success", response.data);
                //         this.$bus.$emit('getUsers', response.data.items);
                //     },
                //     error => { 
                //         console.log("fail", error.message);
                //     }
                // )
                axios.get(`http://localhost:8000/myapp/search?query=${this.query}`).then(
                    response => {
                        console.log("success", response.data);
                        this.$bus.$emit('getResults', response.data.papers);
                    },
                    error => { 
                        console.log("fail123", error.message);
                    }
                )
            }
		}
	},
    mounted(){
        this.query = this.$route.query.query;
        document.title = this.query + ' - Search'
        if(this.query.length > 0){
            this.send_query()
        }
        
    },
    
}
</script>

<style scoped>
.outer_box{
    width: 800px;
    height: 50px;
    margin-top: 30px;
    margin-left: 30px;
}

.icon_box{
    display: inline;
    width: 300px;
    float: left;
}

.logo_img{
    height: 40px;
}

.search_box{
    position: relative;
    width: 500px;
    float: left;
    height: 30px;
}

.search_img{
    position: absolute;
    top: 11px;
    left: 12px;
    height: 17px;
}

.search_box input{
    width: 100% ;
    height: 35px;
    border-width: 1px;
    border-style: solid;
    border-radius: 10px;
    border-color: gainsboro;
    font-size: 14px;
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
    height: 39px;
    border: none;
    background-color: rgb(78, 110, 242);
    color: white;
    border-radius:10px;
    outline: none;
    width: 100px;
    font-size: 18px;
    padding: 5px;
}

.search_box button:HOVER{
    background-color: #2b56f0;
}

.advanceBtn{
    position: relative;
    top: 0px;
}

</style>