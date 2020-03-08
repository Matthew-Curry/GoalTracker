<template>
    <div>
        <h1 style = "font-size: 27px">From the 5 categories below, pick those that are most important to you (max 3)</h1>
            <input type="checkbox" name="goal" value="fitness" v-model="prio" :disabled="prio.length==3">Fitness<br />
            <input type="checkbox" name="goal" value="social" v-model="prio" :disabled="prio.length==3">Social<br />
            <input type="checkbox" name="goal" value="education" v-model="prio" :disabled="prio.length==3">Education<br />
            <input type="checkbox" name="goal" value="career" v-model="prio" :disabled="prio.length==3">Career<br/>
            <input type="checkbox" name="goal" value="hobby" v-model="prio" :disabled="prio.length==3">Hobby<br/>
            <button @click = "submitCat">Submit</button>
    </div>
</template>

<script>
export default {
    name: "SelectCategories",
    data(){
        return{
        prio: []
    }
    },
    methods: {
        //a method that emits
        submitCat(){
            this.$emit('selectClicked', this.prio)
        }
    }

}
</script>