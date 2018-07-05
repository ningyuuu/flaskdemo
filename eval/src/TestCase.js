import React, { Component } from 'react';
import PropTypes from 'prop-types';

class TestCase extends Component {
  render() {
    return (
      <tr>
        <td>{this.props.file}</td>
        <td>{this.props.body}</td>
        <td>{this.props.correctAns}</td>
        <td>{this.props.result}</td>
      </tr>
    );
  }
}

TestCase.propTypes = {
  file: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
  correctAns: PropTypes.number.isRequired,
  result: PropTypes.string.isRequired
}

export default TestCase;