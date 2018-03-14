'use strict';
var http = require('http');

/***************************************************************
* AJAX request wrapper function
* @param url : String  URL to send/receive AJAX request (relative)
* @param method : String  HTTP Method to use (POST, GET)
* @param content : String  Content headers to send/receive
* (application/xml, application/json)
* @param result: Object  Result object (i.e. ordered_posts, posts['title'])
*
*****************************************************************/

var ajaxRequest = function(url, method, content, result) {
	if (method !== 'POST' || method !== 'GET') {
		throw ReferenceError;
	}
	$.ajax({
		type: method,
		url: url,
		contentType: content,
		data: result,
		success: function(response) {
			if (response) {
				$('#result').html(response);
			}
		}
	});
}

module.exports(ajaxRequest);

