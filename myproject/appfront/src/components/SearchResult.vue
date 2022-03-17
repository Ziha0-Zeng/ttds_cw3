<template>
<div>
    <div v-for="(paper,index) in papers.slice((curpage - 1) * pagesize, curpage*pagesize)" :key="paper.title" class="paperBox"> 
		<div v-show="paper.isShown===1">
			<div><a :href="paper.url"><h4 class="title"> {{paper.title}} </h4> </a></div>
			<div class = "authors"> {{paper.authors}} </div>
			<div class = "abstract"> {{paper.abstract.substring(0,270)}}...</div>
			<span><el-button size="small" circle class="rate_btn" @click="goodEvent(index)"><img src="../assets/good.png" class="rate_img"></el-button></span>
			<span><el-button size="small" circle @click="badEvent(index)"><img src="../assets/bad.png" class="rate_img"></el-button></span>
		</div>
	</div>
    <div class="pagination">
		<el-pagination
		background
		@size-change="handleSizeChange"
		@current-change="handleCurrentChange"
		:current-page="1"
		:page-size="pagesize"
		layout="total, sizes, prev, pager, next, jumper"
		:total="papers.length"
		>
		</el-pagination>
    </div>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name:"SearchResult",
    methods: {
		handleSizeChange(val) {
			console.log(`每页 ${val} 条`);
			this.pagesize = val;
		},

		handleCurrentChange(val) {
			console.log(`当前页: ${val}`);
			this.curpage = val;
			window.scrollTo(0,0)
		},

		goodEvent(index){
			axios.get(`http://localhost:8000/myapp/feedback?goodFeedback=${this.papers[index].title}`)
		},

		badEvent(index){
			this.papers[index].isShown = 0
			axios.get(`http://localhost:8000/myapp/feedback?badFeedback=${this.papers[index].title}`)
		},

		
    },
    data() {
      return {
        papers:[],
        curpage:1,
        pagesize:10,
        filterMethod: 0,
      };
    },

    mounted() {
      this.$bus.$on('getResults', (papers)=>{
        this.papers = papers;
      })

      this.$bus.$on('filter', (filterMethod)=>{
        this.filterMethod = filterMethod;
      })
    },

    watch: {
      filterMethod: function (){
        console.log("filter method changes")
      }
    }


}
</script>

<style scoped>
.pagination{
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    text-align: center;
    width: 70%;
    max-width: 7500px;
    min-width: 600px;
   
}

.paperBox{
    width: 70%;
    max-width: 750px;
    min-width: 600px;
}

.title{
    color: blue;
    margin-top: 10px;
    margin-bottom: 10px;
}

.authors{
    color: #006621;
    font-size: 14px;
}

.abstract{
    margin-top: 10px;
    margin-bottom: 10px;

    font-size: 14px;
}

.rate_img{
    height: 17px;
}

.rate_btn{
    margin-bottom: 30px;
    margin-right: 15px;
}

</style>