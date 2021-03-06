class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="application">
                <h1>twitXiv</h1>
                <p id="subtitle">Stay up-to-date on the most buzzed about papers posted to Twitter in the past 7 days.</p>
                <p id="bot-link"><a href="https://twitter.com/twitXiv">Follow the Twitter bot!</a></p>
                <TweetContainer/>
            </div>
        )
    }
}

class Tweet extends React.Component {
    constructor(props) {
        super(props);
        this.tweet_id = this.props.key;
        this.data = this.props.data;
    }

    getColor() {
        const createdAt = new Date(this.data.created_at);
        const now = new Date();
        const age = Math.min(7, (now - createdAt) / (1000 * 60 * 60 * 24));  // days
        const expAge = Math.exp(age/7)/Math.E;
        const green = 192 + Math.round(12 * (1 - expAge));
        const red = 192 - Math.round(0 * (1 - age/7)) - Math.round(50 * (1 - expAge));
        const blue = 192 + Math.round(63 * (1 - expAge));
        const styleStr = `rgb(${red}, ${green}, ${blue})`;
        return styleStr;
    }

    generateContent() {
        let content = this.data.text;
        for(const urlData of this.data.urls) {
            content = content.replace(urlData.url, `<a href=${urlData.expanded_url} target="_blank">${urlData.display_url}</a>`);
        }
        return (<div className="tweet-content" dangerouslySetInnerHTML={{__html: content}}></div>)
    }

    generateFooter() {
        return (
            <div className="tweet-footer">
                <span className="tweet-reply-counter">💬 {this.data.reply_count}</span>
                <span className="tweet-retweet-counter">🔁 {this.data.retweet_count + this.data.quote_count}</span>
                <span className="tweet-like-counter">❤️ {this.data.like_count}</span>
            </div>
        )
    }

    render() {
        return (
            <div className="tweet">
                <div className="tweet-body" style={{backgroundColor:this.getColor()}}>
                    <div className="tweet-header">
                        <span className="author-name">{this.data.author_data.name}</span>
                        <span className="author-username">@{this.data.author_data.username}</span>
                        <a className="tweet-link" href={`https://twitter.com/user/status/${this.data.id}`} target="_blank">Tweet</a>
                    </div>
                    <br/>
                    {this.generateContent()}
                    <br/>
                    {this.generateFooter()}
                </div>
            </div>
        );
    }
};

class TweetContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tweetData: [],
        }
        this.getTweets();
    }

    updateTweets(data) {
        this.setState({'tweetData': data});
    }

    getTweets(sortBy='likes') {
        console.log(this);
        $.ajax('/query_tweets/' + sortBy, {
            success: (data) => {this.updateTweets(data)},
        });
    }

    renderTweet(data) {
        return (
            <Tweet key={data.id} data={data}/>
        );
    }

    render() {
        return (
            <div className="tweet-container">
                <div className="content-header">
                    <div className="sort-controls">Sort by:
                        <button onClick={() => this.getTweets('likes')}>Likes</button>
                        <button onClick={() => this.getTweets('retweets')}>Retweets</button>
                        <button onClick={() => this.getTweets('replies')}>Replies</button>
                    </div>
                    <div className="tweet-age-key">
                        <span className="tweet-age-key-old">Old</span>
                        <span className="tweet-age-key-new">New</span>

                    </div>
                </div>
                <div className="tweet-container-content">
                    {this.state.tweetData.map((data) => this.renderTweet(data))}
                </div>
            </div>
        )
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('application-container')
);
