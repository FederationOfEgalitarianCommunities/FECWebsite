var browserSync = require('browser-sync').create();
var exec = require('child_process').exec;
var gulp = require('gulp');


var virtualEnvActivate = '~/.virtualenvs/fec/bin/activate';

var watchPaths = [
  'fec/**/*.css',
  'fec/**/*.html',
  'fec/**/*.js',
  'fec/**/*.less',
  'fec/**/*.py',
];


gulp.task('default', ['django-server', 'proxy-server']);

gulp.task('django-server', function(cb) {
  var proc = exec(
    'source ' + virtualEnvActivate + '; ' +
    'cd fec; PYTHONUNBUFFERED=1 python manage.py runserver 0.0.0.0:8000'
  );
  proc.stdout.on('data', function(data) { process.stdout.write(data); });
  proc.stderr.on('data', function(data) { process.stdout.write(data); });
  return cb();
});

gulp.task('proxy-server', function() {
  return browserSync.init(watchPaths, {
    proxy: '0.0.0.0:8000',
    port: 8010,
    open: false,
  });
});

