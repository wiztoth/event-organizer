<template>
    <div class="container">
      <center> 
        <select v-model="selected" name="selected" @change="updateButton">
            <option disabled value="">Please select one</option>
            <option v-for="option in options" :value="option.event_name" >{{ option.event_name }}</option>
        </select><br><br>
        <button :disabled="enabled == 1" class="viewdata" @click="fetchData()">View Guests</button>
      </center>
          
      <br>
         
      <VueTable v-if="hide_table" :headers="headers" :keys="keyValue" :data="this.event_guests">
        <template #th>
            <th scope="col" class="px-6 py-3"> Actions </th>
        </template>
        <template #td="{ item }">
            <td class="flex">
                <DeleteIcon @click="deleteItem(item.id)" />
                <EditIcon @click="edit(item)" />
            </td>
        </template>
      </VueTable>
    
      <p v-else> <i>No data to display, please select an event from the dropdown menu</i></p>
    </div>
</template>
<style>
body{
    color: #000;
}
.viewdata{

  background-color: #4584eb;
  color: rgb(255, 255, 255);
  padding: 5px 5px;
  border: none;
  text-align: center;
  border-radius: 4px;
  cursor: pointer;

}
select {
  appearance: none;
  /*  safari  */
  -webkit-appearance: none;
  /*  other styles for aesthetics */
  width: 100%;
  padding: 0.675em 6em 0.675em 1em;
  background-color: #fff;
  border: 1px solid #caced1;
  border-radius: 0.25rem;
  color: #000;
  cursor: pointer;
}
</style>


<script>
import axios from 'axios';
export default {
    data() {
    return {
      selected: '',
      options: [],
      event_guests: [],
      hide_table: false,
      enabled: 1
    }
  },
  methods:{
    loadOptions(){
      axios.get('http://localhost:5000/api/events')
        .then((response) => {
          this.options = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    async fetchData(){
        this.clearTable();
        const collection_name = this.selected;
        this.hide_table = true;
        const querySnapshot = await getDocs(collection(db, "database", "eventi", collection_name));
        querySnapshot.forEach((doc) => {
        // doc.data() is never undefined for query doc snapshots
            console.log(doc.id, " => ", doc.data());
            this.event_guests.push(doc.data());
            
        });
    },
    clearTable() {
    this.event_guests.splice(0);
  },
  updateButton() {
      if (this.selected !== 'Please select one') {
        this.enabled = 0;
      } else {
        this.enabled = 1;
      }
    }
},
mounted() {
      this.loadOptions();
      
  }
  }



</script>


<script setup>
    import { VueTable  } from "@harv46/vue-table"
    import { onMounted, ref } from "vue";
    import { db } from '../firebase/init.js';
    import { collection, getDocs, doc} from "firebase/firestore";
    import "@harv46/vue-table/dist/style.css"
    const headers = ["Nome", "Evento", "Email", "Numero", "Metodo di pagamento", "€"];
    const keyValue = [
        "name",
        "selected",
        "email",
        "phone",
        "payment",
        "euro"
        
    ];


    
    
</script>

