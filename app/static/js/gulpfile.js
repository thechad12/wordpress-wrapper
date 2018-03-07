var gulp = require('gulp'),
	concat = require('gulp-concat'),
	uglify = require('gulp-uglify')
	css = require('gulp-minify-css');

gulp.task('concat-scripts', function() {
	gulp.src('./scripts/*.js')
	.pipe(concat('main.js'))
	.pipe(gulp.dest('./main'));
});

gulp.task('minify', function() {
	gulp.src('./main/main.js')
	.pipe(uglify())
	.pipe(gulp.dest('./main/main.min.js'));
});