import React from "react"
import './InputHandler.css';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";


export default function InputHandler() {
    const [prompt, setPrompt] = useState('');
    const [chapters, setChapters] = useState('');
    const [gptKey, setGptKey] = useState('');
    const navigate = useNavigate();



    const handleSubmit = (event) => {
        event.preventDefault();
        status = sendDataToServer(prompt, chapters, gptKey);
        //TODO: Check Status

    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        if (name === 'prompt') {
            setPrompt(value);
        } else if (name === 'chapters') {
            setChapters(value);
        } else if (name === 'gptKey') {
            setGptKey(value);
        }
    };

    const sendDataToServer = async (prompt, chapters, gptKey) => {
        const userInput = {
            prompt,
            chapters,
            gptKey,
        };

        await fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userInput),
        });
        console.log("Finished Sending")
        
        navigate("/download")

        return true


        // Handle the response from the backend
    };

    return (

        <div>
            <h1>Book Create GPT</h1>

            <div className="inputContainer">
                <label>
                    <span className="promptText">Prompt</span>
                    <input
                        name="prompt"
                        className="inputField"
                        value={prompt}
                        onChange={handleInputChange}
                    />
                </label>
            </div>

            <div className="inputContainer">
                <label>
                    <span className="promptText">Number of chapters</span>
                    <input
                        name="chapters"
                        className="inputField"
                        value={chapters}
                        onChange={handleInputChange}
                    />
                </label>
            </div>

            <div className="inputContainer">
                <label>
                    <span className="promptText">GPT Key</span>
                    <input
                        name="gptKey"
                        className="inputField"
                        value={gptKey}
                        onChange={handleInputChange}
                    />
                </label>
            </div>

            <button type="submit" onClick={handleSubmit}>
                Submit
            </button>
        </div>



    )



}