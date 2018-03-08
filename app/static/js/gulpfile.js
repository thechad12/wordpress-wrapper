'use strict';

var gulp = require('gulp'),
	concat = require('gulp-concat'),
	uglify = require('gulp-uglify'),
	css = require('gulp-minify-css'),
	runSeq = require('run-sequence');

/*************************************************
* Gulp tasks
* enter respective task in terminal to run
* @function concat-scripts : Run gulp concat-scripts to concatenate
* @function minify : Run gulp minify to minify javascripts
* @function concat-css : Concatenates CSS files
* @function minify-css : Minifies CSS
* @function heroku : Runs for production deploys
*
***************************************************/

gulp.task('concat-scripts', function() {
	gulp.src('./scripts/*.js')
	.pipe(concat('main.js').on('error', function(e) {
		console.log(e);
	}))
	.pipe(gulp.dest('./main'));
});

gulp.task('minify', function() {
	gulp.src('./main/main.js')
	.pipe(uglify().on('error', function(e) {
		console.log(e);
	}))
	.pipe(gulp.dest('./main'));
});

gulp.task('concat-css', function() {
	gulp.scr('../css/*.css')
	.pipe(concat('main.css').on('error', function(e) {
		console.log(e);
	}))
	.pipe(gulp(dest('../css/main')));
});

gulp.task('minify-css', function() {
	gulp.src('../css/main/main.css')
	.pipe(uglify().on('error', function(e) {
		console.log(e);
	}))
	.pipe(gulp.dest('../css/main'));
});

gulp.task('heroku', function() {
	runSeq('concat-scripts', 'minify', 'concat-css', 'minify-css')
	.on('error', function(e) {
		console.log(e);
	});
});
