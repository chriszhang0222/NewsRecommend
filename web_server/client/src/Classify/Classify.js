import React, { Component } from 'react';

class ClassifyPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            text: '',
            classify: null
        }
        this.processInput = this.processInput.bind(this);
    }

    processInput(event){
        if(event.key === 'Enter'){
            let text = event.target.value;
            fetch('http://localhost:5000/news/classify', {
                method: 'POST',
                cache: 'no-cache',
                headers: {
                      'Accept': 'application/json',
                      'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text
                })
            }).then((res) => res.json())
                    .then((res) => {
                        this.setState({
                            classify: res
                        })
                    })
        }
    }
    render(){
        return (
            <div>
                <div className='container'>
                    <div className='row in-box'>
                        <div className='input-field'>
                            <input type='text'
                                   onKeyPress={e => this.processInput(e)}
                                   />
                        </div>
                    </div>
                    <p className='result'>{ this.state.classify }</p>
                </div>
            </div>
        )
    }
}

export default ClassifyPage