// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, setDoc, doc, collection } from "firebase/firestore";
 

const firebaseConfig = {
  apiKey: "AIzaSyAH09nmaDLspqWcmhFHw8BPMfOh3ZHyvOM",
  authDomain: "event-organizer-bf1ea.firebaseapp.com",
  projectId: "event-organizer-bf1ea",
  storageBucket: "event-organizer-bf1ea.appspot.com",
  messagingSenderId: "58473919738",
  appId: "1:58473919738:web:9a61c434aee79fc09b0543",
  measurementId: "G-W6L97PF1YJ"
};
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const guests = collection(db, "event-guests");
export {guests, db}
 


