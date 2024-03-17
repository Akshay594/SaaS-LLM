import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [query, setQuery] = useState('');

    const sendMessage = async (e) => {
        e.preventDefault();
        const newMessages = [...messages, { user: 'You', text: query }];
        setMessages(newMessages);
        setQuery('');

        try {
            const response = await axios.post('http://127.0.0.1:8000/make_query/', {
                query: query,
                file_name: 'marksheet.csv', // Adjust as needed
            });
            setMessages([...newMessages, { user: 'Bot', text: JSON.stringify(response.data.response) }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages([...newMessages, { user: 'Bot', text: 'Error processing your query.' }]);
        }
    };

    return (
        <div className="p-4">
            <div className="mb-4">
                {messages.map((message, index) => (
                    <div key={index} className={`mb-2 ${message.user === 'You' ? 'text-right' : 'text-left'}`}>
                        <span className="inline-block rounded px-4 py-2 text-white bg-blue-600">
                            {message.text}
                        </span>
                    </div>
                ))}
            </div>
            <form onSubmit={sendMessage} className="flex">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="flex-1 p-2 border-2 border-gray-200"
                />
                <button type="submit" className="p-2 bg-blue-500 text-white">
                    Send
                </button>
            </form>
        </div>
    );
};

export default Chat;
