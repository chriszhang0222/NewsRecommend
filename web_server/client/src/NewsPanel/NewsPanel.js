import React, {Component} from 'react'
import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';
import Auth from '../Auth/Auth';
import _ from 'lodash';

class NewsPanel extends Component{
    constructor(){
        super();
        this.state = {news: null, func:[],  pageNum: 0,};
        this.handleScroll = this.handleScroll.bind(this);
    }

    componentDidMount(){
        this.loadMoreNews();
        this.loadMoreNews = _.debounce(this.loadMoreNews, 500);
        window.addEventListener('scroll', this.handleScroll);
    }

    handleScroll(){
        let scrolY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if((window.innerHeight+scrolY) >= (document.body.offsetHeight-50)){
            console.log('loading more news');
            this.loadMoreNews();
        }
    }

    loadMoreNews(){
        let url = 'http://localhost:5000'+
      '/news/userId/' + Auth.getEmail() + '/pageNum/' + this.state.pageNum;

        fetch(url)
            .then((res) => {
                let i = res;
                return res.json();
            })
            .then(news => {
                this.setState({
                    news: this.state.news ? this.state.news.concat(news) : news,
                    pageNum: this.state.pageNum + 1
                });
            });
    }

    renderNews(){
        var news_list = this.state.news.map(function(news){
           return(
             <a className='list-group-item'  href="#">
                 <NewsCard news={news} />
             </a>
           );
        });

        return(
            <div className="container-fluid">
                <div className='list-group'>
                    {news_list}
                </div>
            </div>
        );
    }

    render(){
        if(this.state.news){
            return(
                <div>
                    {this.renderNews()}
                </div>
            );
        } else{
            return(
                <div>
                    <div id='msg-app-loading'>
                        <h2>Loading...</h2>
                    </div>
                </div>
            );
        }
    }
}

export default NewsPanel;
