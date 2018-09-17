var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  news = [
      {
          'title': "Inside Andrew falied",
          'description': "In the end, ......",
          'source': 'cnn',
          'url':'https://www.google.co.jp/imgres?imgurl=https%3A%2F%2Fstatic.gamespot.com%2Fuploads%2Fscreen_small%2F1197%2F11970954%2F3434870-trailer_nba2k19_crown_20180905.jpg&imgrefurl=https%3A%2F%2Fwww.metacritic.com%2Fgame%2Fplaystation-4%2Fnba-2k19&docid=g-FCoGVlpWYAQM&tbnid=_1uZ1sbh_Ixd4M%3A&vet=10ahUKEwi09IrQr8DdAhV8FzQIHa5zCvgQMwi2AigiMCI..i&w=320&h=180&bih=747&biw=1294&q=nba&ved=0ahUKEwi09IrQr8DdAhV8FzQIHa5zCvgQMwi2AigiMCI&iact=mrc&uact=8',
          'urlToImage': 'https://washington-org.s3.amazonaws.com/s3fs-public/styles/editorial_wide/public/the-white-house-north-lawn-plus-fountain-and-flowers-credit-stephen-melkisethian_flickr-user-stephenmelkisethian.jpg?itok=ElC-_6Hr',
          'reason': "Recommand",
          'digest':"ghsd78eer",
          'time':'today'
      },
      {
          'title':"Hello hello hey",
          'description':"Finally, she does......",
          'url':"https://www.google.co.jp/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwjArKDVr8DdAhWaCTQIHUjjD-8QjRx6BAgBEAU&url=http%3A%2F%2Fwww.sportingnews.com%2Fus%2Fnba%2Fnews%2Fnba-playoffs-2018-odds-predictions-to-win-nba-finals-warriors-cavs-rockets-raptors-first-round%2F1s55sn4tgueom1sqh96flou7ck&psig=AOvVaw28GB9uOSrmL6AK8fydh0MQ&ust=1537216440259672",
          'urlToImage':'http://images.performgroup.com/di/library/sporting_news/e0/f0/lebron-james-ftr-020118jpg_1wtwr9c28lo281p8aunkukylr0.jpg?t=1370642737&w=960&quality=70',
          'source':'cnn',
          'reason':'hot',
          'digest':"fdf8sjdk3",
          'time':'wednesday'
      }
  ];
  res.json(news);

});

module.exports = router;
