<template>
    <div>
        <QueryInput> </QueryInput>
        <AdvancedSearch class="advancedSearch"></AdvancedSearch>
        <FilterElement></FilterElement>
        <SearchResult class="seachResult"> </SearchResult>
    </div>
</template>

<script>
import QueryInput from '../components/QueryInput'
import SearchResult from '../components/SearchResult'
import AdvancedSearch from '../components/AdvanceSearch'
import FilterElement from '../components/FilterElement'
export default {
    name:'MainSearchInterface',
    
    components:{QueryInput, SearchResult, AdvancedSearch, FilterElement}
    
}
</script>

<style scoped>
.advancedSearch{
    position: relative;
    left: 330px;
}

.seachResult{
    margin-left: 300px;
}
</style>