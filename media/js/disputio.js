/* javascript */

var d_slider_speed = 360;

$(document).ready(function()
{
	$('#submit-box').hide();
	$('#key-viewer-box').hide();
	
	function new_part(e){
		var nki = $('#new-key-input');
		var keyval = nki.val();
		nki.val('');
		
		var key = $('<div class="part-key">'+keyval+'</div>')
		var value = $('<div class="value-box"><div class="part-value-label">'+keyval+'</div><textarea class="part-value" name="'+keyval+'"></textarea></div>')
		
		$('#new-key-box').append(key);
		$('#edit-box').append(value);
		$('#submit-box').show();
	}
	
	
	$('#new-key-submit').on('click', new_part);
	
	$('#submit-box').on('click', function(e){
		$('#root').submit();
	});
	
	$('#doclist-box').load('/disputio/docs', function(responseText, textStatus, XMLHttpRequest){
		$('.key-item').on('click', function(e){
			var that = $(this);
			var url = encodeURI(that.attr('title'));
			$('#key-viewer-paper').load(url, {d:0}, function()
			{
				$('#doclist-box').hide('slide',{direction:'left'}, d_slider_speed, function(){
					$('#key-viewer-box').show('slide',{direction:'right'}, d_slider_speed);
				});
			});
		});
	});
	
	$('#key-viewer-close').on('click', function(e){
		$('#key-viewer-box').hide('slide',{direction:'right'}, d_slider_speed, function(){
			$('#doclist-box').show('slide',{direction:'left'}, d_slider_speed);
		});
	});
	
	
});
