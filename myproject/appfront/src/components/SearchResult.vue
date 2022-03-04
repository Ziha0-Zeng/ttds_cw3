<template>
  <div>
      <div v-for="paper in papers.slice((curpage - 1) * pagesize, curpage*pagesize)" :key="paper.title" class="paperBox"> 
        <div><h4 class="title"> {{paper.title}} </h4> </div>
        <div class = "authors"> {{paper.authors}} </div>
        <div class = "abstract"> {{paper.abstract.substring(0,270)}}... </div>
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

export default {
    name:"SearchResult",
    methods: {
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.curpage = val;
        window.scrollTo(0,0)
      }  
    },
    data() {
      return {
        papers:[],
        curpage:1,
        pagesize:10,
        rankMethod: 0,
        filterMethod: 0
      };
    },

    mounted() {
      this.$bus.$on('getResults', (papers)=>{
        console.log("mount")
        this.papers = papers;
      })

      this.$bus.$on('rank', (rankMethod)=>{
        console.log("mount2")
        this.rankMethod = rankMethod;
      })

      this.$bus.$on('filter', (filterMethod)=>{
        console.log("mount3")
        this.filterMethod = filterMethod;
      })
    },

    watch: {
      filterMethod: function (){
        console.log("filter method changes")
      },
      rankMethod: function (){
        console.log("rank method changes")
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
    margin-bottom: 30px;

    font-size: 12px;
}

</style>