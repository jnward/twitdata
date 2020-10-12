/*** @jsx React.DOM */

var nextToken = 'head';
var loading = 0;

var realPython = React.createClass({
    render: function() {
      return (<h2>Greetings, from Real Python!</h2>);
    }
});


class Tweet extends React.Component {
    constructor(props) {
        super(props);
        this.tweet_id = this.props.tweet_id;
    }

    componentDidUpdate() {
        console.log('Updated' + this.tweet_id);
        twttr.widgets.load(document.getElementById("container"));
    }

    render() {
        return (<blockquote class="twitter-tweet"><a href={"https://twitter.com/x/status/" + this.tweet_id}></a></blockquote>);
    }
};

const tweet = new Tweet(999);

ReactDOM.render(
    <Tweet tweet_id="463440424141459456"/>,
    document.getElementById('content')
);

const tweets_pane = document.getElementById("tweets");


function displayTweets(tweet_ids) {
    // display embeded tweets given list of ids
    for(tweet_id of tweet_ids) {
        console.log(tweet_id);
        twttr.widgets.createTweet(tweet_id.toString(), tweets_pane)
        .then(function() {
            console.log('tweet added');
            loading -= 1;
        })
    }
};


$(window).scroll(function() {
//    console.log('scrolling');
//    console.log($(window).scrollTop());
//    console.log($(document).scrollHeight);
//    console.log($(document).height());
//    console.log($(window).scrollTop());
//    console.log($(window).height());
    if($(window).scrollTop() + 3*$(window).height() >= $(document).height() - 0 && !loading) {
        loading += 10;
        console.log('got to bottom!');
        $.ajax('/load_tweets/' + nextToken, {
            success: function(data) {
                displayTweets(data.tweet_ids);
                nextToken = data.next_token;
                console.log(data);
            },
            error: function() {
                console.log('error');
        }
    });
    }
});


const nextButton = $('#next-button')
nextButton.click(function() {
    $.ajax('/load_next/test_token', {
        success: function(data) {
            displayTweets(data.tweet_ids);
            console.log(data);
        },
        error: function() {
            console.log('error');
        }
    });
    console.log('Button clicked');
});

$(document).ready(function() {
    loading += 10;
    $.ajax('/load_tweets/' + nextToken, {
        success: function(data) {
            displayTweets(data.tweet_ids);
            nextToken = data.next_token;
            console.log(data);
        },
        error: function() {
            console.log('error');
        }
    });
});


//displayTweets([20,21,22,23,24,25]);