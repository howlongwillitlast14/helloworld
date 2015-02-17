$(function(){

	$('#search').keyup(function(){
		$.ajax({
			type: 'POST',
			url: "/articles/search/",
			data: {
				'search_text' : $('#search').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,  //if it succeeds this searchSuccess callback function would be called
			dataType: 'html'
		});
	});

});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search-results').html(data);
}