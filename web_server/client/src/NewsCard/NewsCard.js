import React, {Component} from 'react';
import './NewsCard.css';
import { classTitle, classColor } from '../newsSettings.js';
import defaultPic from './default.jpg';
import Auth from "../Auth/Auth";

class NewsCard extends Component{
    redirectToUrl(url){
        this.sendClickLog();
        window.open(url, '_blank');
    }

    sendClickLog(){

        const url =
			'http://localhost:5000' +
			'/news/userId/' +
			Auth.getEmail() +
			'/newsId/' +
			this.props.news.digest;
		console.log(url);
		let request = new Request(encodeURI(url), {
			method: 'POST'
		});

		fetch(request);
    }

    defaultImg(e){
        e.target.src = defaultPic;
    }

    render(){
        return (
            <div className='col s12 m6 l4'>
                <div className='card medium'>
                    <div className='card-image fill'>
                        {
                            this.props.news.urlToImage && (
                                <img
                                className='img200'
                                src={this.props.news.urlToImage}
                                onError={this.defaultImg}/>
                            )
                        }
                        {!this.props.news.urlToImage && (
							<img className="img200 default" src={defaultPic} />
						)}
						<span className='card-title'>
                            <div className='title'
                            onClick={() => this.redirectToUrl(this.props.news.url)}>
                                {this.props.news.title}
                            </div>
                        </span>
                    </div>
                    <div className='card-content'>
                        <p> {this.props.news.description} </p>
                    </div>
                    <div className='card-action'>
                        {this.props.news.source != null && (
							<div className={'source labels'}>{this.props.news.source}</div>
						)}
						 {this.props.news.reason != null && (
                                        <div className="chip light-green news-chip">
                                            {this.props.news.reason}
                                        </div>
                        )}
                        {this.props.news.reason2 != null && (
                                        <div className="chip light-blue news-chip">
                                            {this.props.news.reason2}
                                        </div>
                        )}
						{this.props.news.time != null && (
							<div className="amber darken-1 labels">Today</div>
						)}
						{this.props.news.class != null && (
							<div
								className="news-class-banner"
								style={{
									background: classColor[this.props.news.class]
								}}
							>
								{classTitle[this.props.news.class]}
							</div>
						)}
                    </div>
                </div>
            </div>
        );
    }


    // render(){
    //     return(
    //       <div className="news-container" onClick={()=> this.redirectToUrl(this.props.news.url)}>
    //         <div className="row">
    //             <div className="col s4 fill">
    //                 <img src={this.props.news.urlToImage} alt="news"/>
    //             </div>
    //             <div className="col s8">
    //                 <div className="news-intro-col">
    //                     <div className="news-intro-panel">
    //                         <h4>{this.props.news.title}</h4>
    //                         <div className="news-description">
    //                             <p>{this.props.news.description}</p>
    //                             <div>
    //                                 {this.props.news.source != null && (
    //                                     <div className="chip light-blue news-chip">
    //                                         {this.props.news.source}
    //                                     </div>
    //                                 )}
    //                                 {this.props.news.reason != null && (
    //                                     <div className="chip light-green news-chip">
    //                                         {this.props.news.reason}
    //                                     </div>
    //                                 )}
    //                                 {this.props.news.time != null && (
    //                                     <div className="chip amber news-chip">
    //                                         {this.props.news.time}
    //                                     </div>
    //                                 )}
    //                             </div>
    //                         </div>
    //                     </div>
    //                 </div>
    //             </div>
    //         </div>
    //       </div>
    //     );
    // }
}


export default NewsCard;