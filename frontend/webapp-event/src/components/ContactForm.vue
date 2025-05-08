<template>
    <div class="container">
        <form @submit.prevent="addGuest">
          <label>Guest Name:</label>
          <input 
            type="text" 
            v-model="name"
            name="name"
          >
          <label>Event Name:</label>
          <select v-model="selected" name="selected">
            <option disabled value="">Please select one</option>
            <option v-for="option in options" :value="option.event_name" >{{ option.event_name }}</option>
          </select>
         
          <br><br>
          <label>Email:</label>
          <input 
            type="email" 
            v-model="email"
            name="email"
           >
           <label>Phone Number:</label>
          <input 
            type="text" 
            v-model="phone"
            name="phone"
          >
          <label>Payment Method:</label>
          <input 
            type="text" 
            v-model="payment"
            name="payment"
          >
          <label>Amount (€):</label>
          <input 
            type="text" 
            v-model="euro"
            name="euro"
          >
          
          <input type="submit" value="Add">
        </form>
    </div>
</template>

<style scoped>
* {box-sizing: border-box;}

.container {
  display: block;
  margin:auto;
  text-align: center;
  color: black;
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
  width: 50%;
}

label {
  float: left;
  color: rgb(78, 135, 209);
}

input[type=text], [type=email], textarea {
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  margin-top: 6px;
  color: #3f4d8f;
  margin-bottom: 16px;
  resize: vertical;
}

input[type=submit] {
  background-color: #4584eb;
  color: rgb(255, 255, 255);
  padding: 5px 5px;
  border: none;
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
input[type=submit]:hover {
  background-color: #2b6bc5;
}
</style>

<script>
import { db } from '../firebase/init.js';
import { setDoc , doc } from "firebase/firestore"; 
import axios from 'axios';




export default {
  name: 'ContactUs',
  
  data() {
    return {
      selected: '',
      options: [],
      collections: '',
      name: '',
      email: '',
      phone: '',
      payment: '',
      euro: ''
    }
  },

  methods: {
    addGuest() {
        console.log(this.selected)
        let path = 'database/eventi/'+this.selected
        setDoc(doc(db, path, this.email), {
        name: this.name,
        email: this.email,
        selected: this.selected,
        phone: this.phone,
        payment: this.payment,
        euro: this.euro
});

      axios.post('http://localhost:5000/api/mail', {
          name: this.name,
          email: this.email,
          selected: this.selected,
          phone: this.phone,
          payment: this.payment,
          euro: this.euro
        })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
        this.email='',
        this.name='',
        this.event='',
        this.phone='',
        this.payment='',
        this.euro=''
    },
    loadOptions(){
      axios.get('http://localhost:5000/api/events')
        .then((response) => {
          this.options = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });
    }
},
mounted() {
      this.loadOptions();
  }
}
</script>




