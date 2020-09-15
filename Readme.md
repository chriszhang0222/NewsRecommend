### News Recommendation application
1. Project schematic diagram  
    
    built a web app providing news recommendation service  

    ![image](https://i.imgur.com/F0wSGse.png)  

    - FrontEnd: React.js
    - BackEnd: Node.js + Python & RPC & TensorFlow
    - DataBase: Redis & MongoDB
    - Web tool: Rabbit MQ, News API


2. Web app building  
    * Creates a frontend build pipeline by "create-react-app" package  
    utilizing [React tool](https://reactjs.org/blog/2016/07/22/create-apps-with-no-configuration.html) to create single-page React application, using materializecss to design front-end framework

    * Authentication: **SHA1** with **SALT**  
    For each user, we generate a random a salt and add it to user’s password. Server-side generated password.All user information are stored in MongoDB  

        >Signup: f(password, salt) = hash(password + salt)  
        >Login: hash([provided password] + [stored salt]) == [stored hash]

    * Generate a Node server by ["express-generator"](https://expressjs.com/en/starter/generator.html) package  
    Front-end react app will get information from Node server and display the news from Node server. Node server get news from Backend Server through RPC requests
    
    ![Data flow](https://i.imgur.com/Lzu6pgs.jpg)  

    * Creates Backend RPC server using **jsonrpclib-pelix** python package(**Python**)  
    Node.js server need **RPC client** to send request and communicate with Backend RPC server, creating rpc_client through [**jayson**](https://www.npmjs.com/package/jayson) package  

    * News Pipeline  
    **Rabbit MQ** "message queue" to fetch and send news messages
        1. News monitor: keep monitoring new news  
            * Get latest news metadate - **NewsAPI**
            * Check if it is already scraped - **Redis** (digest, newsId)
            * Send to queue for next fectching
                
                >{ title: string -news title,
                >  description: string -news description,
                >  text: string -news text,
                >  url: string -news page url,
                >  author: string -news author,
                >  source: string -news source,
                >  publishedAt: date -published date,
                >  urlToImage: string -news image url,
                >  class: string -news category,
                >  digest: string -news MD5 digest
                >}

        2. News fetcher: scrape detailed news from original news source
            * Get scraping task from queue
            * Scrape news - **newspaper3k** (python package)
            * Send to queue for deduping

        3. Dedupe news already fetched and write to MongoDB
            * Get deduping task from queue
            * check if duplicated - **TF-IDF** (python package)
            * Write to database
        
    * News recommendation
        * news topic modeling -**tensorflow**(classify)
        * news recommendation 
            * user click log processing
            * Creating or updating preference model for new user -store in database



