var gulp = require('gulp');
var pkgJson = require('./package.json');
var concat = require('gulp-concat');
var filter = require('gulp-filter');
var uglify = require('gulp-uglify');
var plumber = require('gulp-plumber');
var cssnano = require('gulp-cssnano');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var rename = require('gulp-rename');
var mainBowerFiles = require('main-bower-files');
var env = require('gulp-env');
var runSequence = require('run-sequence');
var exec = require('child_process').exec;
var watch = require('gulp-watch');

var staticDir = pkgJson.name + '/static';

var paths = {
	src: {
		templates: pkgJson.name + '/templates',
		sass: staticDir + '/sass',
		images: staticDir + '/images',
		js: staticDir + '/js'
	},
    dist: {
		js: staticDir + '/dist/js',
		css: staticDir + '/dist/css',
		images: staticDir + '/dist/images'
    }	
}

var jsFiles = [paths.src.js + '/*'];

// Compile JS
gulp.task('js', function() {
	gulp.src(mainBowerFiles().concat(jsFiles))
		.pipe(filter('**/*.js'))
		.pipe(concat('main.js'))
		.pipe(uglify())
		.pipe(gulp.dest(paths.dist.js));
});

// Compile CSS
gulp.task('css', function() {
	gulp.src(mainBowerFiles())
		.pipe(filter('**/*.css'))
		.pipe(concat('vendor.css'))
		.pipe(cssnano())
		.pipe(gulp.dest(paths.dist.css));
});

// Compile SASS
gulp.task('sass', function() {
  return gulp.src(paths.src.sass + '/app.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 version']})) // Adds vendor prefixes
    .pipe(gulp.dest(paths.dist.css))
    .pipe(rename('app.min.css'))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.dist.css));
});

// Run Flask server
gulp.task('runServer', function () {
	env({
	    vars: {
	      FLASK_APP: pkgJson.name + "/app.py",
	      FLASK_DEBUG: 1
	    }
	  })
  exec('flask run', function (err, stdout, stderr) {
    console.log(stdout);
    console.log(stderr);
  });
});

// Watch file changes
gulp.task('watch', function () {
  gulp.watch(paths.src.sass + '/**/*.scss').on('change', function(){
  	runSequence('sass');
  });
  gulp.watch(jsFiles).on('change', function(){
  	runSequence('js');
  });  
});

// Build Task
gulp.task('build', ['js', 'css', 'sass']);

// Build all files, run the server and watch for file changes
gulp.task('default', function () {
  runSequence('build', 'runServer', 'watch');
});