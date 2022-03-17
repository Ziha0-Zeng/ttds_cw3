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
                <template slot="title">Category</template>
                <el-menu-item index="1-1" @click="cateFilter(0)">All</el-menu-item>
                <el-menu-item index="1-2" @click="cateFilter(1)">Astrophysics</el-menu-item>
                <el-menu-item index="1-3" @click="cateFilter(2)">Condensed Matter</el-menu-item>
                <el-menu-item index="1-4" @click="cateFilter(3)">Computer Science</el-menu-item>
                <el-menu-item index="1-5" @click="cateFilter(4)">Economics</el-menu-item>
                <el-menu-item index="1-6" @click="cateFilter(5)" style="height: 120px">Electrical Engineering <br/> and Systems Science</el-menu-item>

                <el-menu-item index="1-7" @click="cateFilter(6)" style="height: 120px">General Relativity and <br/> Quantum Cosmology</el-menu-item>
                <el-menu-item index="1-8" @click="cateFilter(7)">High Energy Physics</el-menu-item>
                <el-menu-item index="1-9" @click="cateFilter(8)">Mathematics</el-menu-item>
                <el-menu-item index="1-10" @click="cateFilter(9)">Nonlinear Science</el-menu-item>
                <el-menu-item index="1-11" @click="cateFilter(10)">Nuclear Experiment</el-menu-item>

                <el-menu-item index="1-12" @click="cateFilter(11)">Physics</el-menu-item>
                <el-menu-item index="1-13" @click="cateFilter(12)">Quantitative Biology</el-menu-item>
                <el-menu-item index="1-14" @click="cateFilter(13)">Quantitative Finance</el-menu-item>
                <el-menu-item index="1-15" @click="cateFilter(14)">Quantum Physics</el-menu-item>
                <el-menu-item index="1-16" @click="cateFilter(15)">Statistics</el-menu-item>

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
        cateFilter(filterVal){
            console.log("cat filter " + filterVal);
            this.$bus.$emit('filter', filterVal);
        },
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