import React, { Component } from 'react';
import request from 'request';
import logo from './logo.svg';
import TestCase from './TestCase';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
      results: '[]'
    };
  }

  handleChange = (e) => {
    this.setState({
      value: e.target.value
    });
  }

  queryEndpoint = (endpoint) => {
    request.post({
      url: 'http://localhost:8081/endpoint',
      form: { endpoint }
    }, (err, res, body) => {
      if (err) {
        console.log('Err', err);
      } else {
        this.setState({
          results: body//JSON.parse(body)
        });
      }
    });
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.queryEndpoint(this.state.value);
  }

  render() {
    const results = [];
    for (let child of JSON.parse(this.state.results)) {
      results.push(<TestCase file={child.file} body={child.body} correctAns={child.correctAns} result={child.result.toString()} key={child.file} />);
    }
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">RCA MNIST Flask App Tester</h1>

          <form onSubmit={this.handleSubmit}>
            <label className="App-intro">
              Input your endpoint: &nbsp;
              <input type='text' name='name' onChange={this.handleChange} />
            </label>
            <input type='submit' value='submit' />
          </form>
        </header>
        <div className='App-intro'>
          <table className='table'>
            <tbody>
              <tr>
                <th>File Name</th>
                <th>Your App's Ans</th>
                <th>Correct Ans</th>
                <th>Result</th>
              </tr>
              {results}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default App;
