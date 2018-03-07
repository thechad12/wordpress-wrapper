'use strict';

var gulp = require('gulp'),
	concat = require('gulp-concat'),
	uglify = require('gulp-uglify'),
	css = require('gulp-minify-css');

/*************************************************
* Gulp tasks
* enter respective task in terminal to run
* @function concat-scripts : Run gulp concat-scripts to concatenate
* @function minify : Run gulp minify to minify javascripts
*
*
***************************************************/

gulp.task('concat-scripts', function() {
	gulp.src('./scripts/*.js')
	.pipe(concat('main.js'))
	.pipe(gulp.dest('./main'));
});

gulp.task('minify', function() {
	gulp.src('./main/main.js')
	.pipe(uglify().on('error', function(e) {
		console.log(e);
	}))
	.pipe(gulp.dest('./main/main.min.js'));
});