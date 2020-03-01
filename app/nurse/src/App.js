import React, { Component } from 'react';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      patientName: '',
      patientID: null,
      patientAge: '',
      patientGender: null,
      VitaminA: '',
      VitaminB: null,
      VitaminC: '',
    };
  }
  myChangeHandler = (event) => {
    let nam = event.target.name;
    let val = event.target.value;
    this.setState({ [nam]: val });
  }

  handleClick(e) {
    e.preventDefault();
    console.log('The link was clicked.');
    // Insert Push Request Here
    // axios.get(`http://127.0.0.1:5000/incoming_request`)
    // .then(res => {
    //   const persons = res.data;
    //   this.setState({ persons });
    // })

    axios({
      method: 'post',
      url: `http://127.0.0.1:5000/incoming_request`,
      data: {
        "patient": {
          "patientName": this.state.patientName,
          "patientID": this.state.patientID,
          "patientAge": this.state.patientAge,
          "patientGender": this.state.patientGender,
        },
        "vitamins-and-minerals": {
          "Vitamin A": this.state.VitaminA,
          "Vitamin B": this.state.VitaminB,
          "Vitamin C": this.state.VitaminC,
        }
      }
    })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render() {
    return (
      <form>
        <h1>Nurse Blood Test Results </h1>
        <p>Patient Name:</p>
        <input
          type='text'
          name='patientName'
          onChange={this.myChangeHandler}
        />
        <p>Patient ID:</p>
        <input
          type='text'
          name='patientID'
          onChange={this.myChangeHandler}
        />
        <p>Patient Age:</p>
        <input
          type='text'
          name='patientAge'
          onChange={this.myChangeHandler}
        />
        <p>Patient Gender: (male/female)</p>
        <input
          type='text'
          name='patientGender'
          onChange={this.myChangeHandler}
        />
        <p>Vitamin A Level:</p>
        <input
          type='text'
          name='VitaminA'
          onChange={this.myChangeHandler}
        />
        <p>Vitamin B Level:</p>
        <input
          type='text'
          name='VitaminB'
          onChange={this.myChangeHandler}
        />
        <p>Vitamin C Level:</p>
        <input
          type='text'
          name='VitaminC'
          onChange={this.myChangeHandler}
        />
        {/* <p>Vitamin D Level:</p>
        <input
          type='text'
          name='VitaminD'
          onChange={this.myChangeHandler}
        />
        <p>Iron Level:</p>
        <input
          type='text'
          name='Iron'
          onChange={this.myChangeHandler}
        />
        <p>Manganese Level:</p>
        <input
          type='text'
          name='Manganese'
          onChange={this.myChangeHandler}
        /> */}

        <br />

        <button onClick={(e) => this.handleClick(e)}>
          Submit
      </button>

      </form>
    );
  }
}

export default App;
