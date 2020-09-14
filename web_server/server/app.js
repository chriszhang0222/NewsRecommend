var cors = require('cors');
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var passport = require('passport');
var config = require('./config/config.json');
var auth = require('./routes/auth');
var indexRouter = require('./routes/index');
var newsRouter = require('./routes/news');
var cors = require('cors');
var app = express();

// view engine setup
app.use(cors());
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');


app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
// app.use(express.static(path.join(__dirname, 'public')));
app.use(
    '/static',
    express.static(path.join(__dirname, '../client/build/static/'))
);

// app.all('*', function(req, res, next){
//   res.header("Access-Control-Allow-Origin", "*");
//   res.header("Access-Control-Allow-Headers", "X-Requested-With");
//   next();
// });

require('./models/main.js').connect(config.mongodbUri);


app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStraregy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStraregy);

const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware);

app.use('/', indexRouter);
app.use('/news', newsRouter);
app.use('/auth', auth);
app.use(cors);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
