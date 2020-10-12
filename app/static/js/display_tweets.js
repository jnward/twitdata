/*** @jsx React.DOM */

class Tweet extends React.Component {
    constructor(props) {
        super(props);
        this.tweet_id = this.props.tweet_id;
        this.text = this.props.text;
        this.categories = ["Cat1", "Cat2"]
    }

    render() {
        return (
            <div className="tweet">
                <div className="tweet-body">
                    <div className="tweet-header">{this.tweet_id}</div>
                    <br/>
                    <div className="tweet-text">{this.text}</div>
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
            tweets.push(
                <Tweet tweet_id={tweetData.tweet_id} text={tweetData.text}/>
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
