/*** @jsx React.DOM */

class Tweet extends React.Component {
    constructor(props) {
        super(props);
        this.tweet_id = this.props.tweet_id;
        this.text = this.props.text;
        this.data = this.props.data;
        this.categories = ["Cat1", "Cat2"]
    }

    generateContent() {
        let urlData;
        let content = this.text;
        for(urlData of this.data.urls) {
            content = content.replace(urlData.url, `<a href=${urlData.expanded_url}>${urlData.display_url}</a>`);
        }
        return <div className="tweet-content" dangerouslySetInnerHTML={{__html: content}}></div>
    }

    render() {
        return (
            <div className="tweet">
                <div className="tweet-body">
                    <div className="tweet-header">
                        <span className="author-name">{this.data.author_data.name}</span>
                        <span className="author-username">@{this.data.author_data.username}</span>
                        <a className="tweet-link" href={`https://twitter.com/user/status/${this.data.tweet_id}`}>Tweet</a>
                    </div>
                    <br/>
                    {this.generateContent()}
                </div>
            </div>
        );
    }
};

class TweetContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tweets: [],
            nextToken: 'head'
        }
        this.handleClick = this.handleClick.bind(this);
        this.updateTweets = this.updateTweets.bind(this);

        this.handleClick();
    }

    updateTweets(data) {
        let tweets = [];
        let tweetData;
        for (tweetData of data.tweets_data) {
            //let text = parseUrls(tweetData.text, tweetData.urls)
            tweets.push(
                <Tweet tweet_id={tweetData.tweet_id} text={tweetData.text} data={tweetData}/>
            );
        }
        this.setState({nextToken: data.next_token});
        this.setState({tweets: this.state.tweets.concat(tweets)});
    }

    handleClick() {
        console.log('click');
        let updateTweets = this.updateTweets;
        $.ajax('/load_tweets/' + this.state.nextToken, {
            success: updateTweets,
            error: function() {
                console.log('error');
            }
        });
    }

    render() {
        return (
            <div className="tweet-container">
                {this.state.tweets}
                <button onClick={this.handleClick}>Get new Tweets</button>
            </div>
        )
    }
}

ReactDOM.render(
    <TweetContainer/>,
    document.getElementById('content')
);
