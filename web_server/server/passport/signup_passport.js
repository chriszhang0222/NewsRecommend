const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;

module.exports = new PassportLocalStrategy(
    {
        usernameField: 'email',
        passportField: 'password',
        passReqToCallback: true
    },

    (req, email, password, done) => {
        const userData = {
            email: email.trim(),
            password: password };

        const newUser = new User(userData);
        newUser.save(err => {
            console.log('Save new User');
            if(err){
                return done(err);
            }
            return done(null);
        });
    }
);