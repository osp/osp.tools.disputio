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
		
// 		$('#new-key-box').append(key);
		$('#edit-box').append(value);
		$('#submit-box').show();
	}
	
	function load_docs()
	{
		$('#doclist-box').load('/disputio/docs', function(responseText, textStatus, XMLHttpRequest){
			$('.key-item').on('click', function(e){
				var that = $(this);
				var url = '/disputio/value_of';
				$('#key-viewer-paper').load(url, {oid:that.attr('title'), key:that.text()}, function()
				{
					$('#doclist-box').hide('slide',{direction:'left'}, d_slider_speed, function(){
						$('#key-viewer-box').show('slide',{direction:'right'}, d_slider_speed);
					});
				});
			});
		});
	}
	
// 	function relate_to(event)
// 	{
// 		var e = event;
// // 		var that = $(this);
// 		var id = e.data.start_point;
// 		var rel = {
// 			relation : 'internal',
// 			start_point: '/id/' + id,
// 			end_point: e.data.end_point.val(),
// 			note: e.data.note.val()
// 		};
// 		$.post('/disputio/add', rel, function(){
// 			e.data.result.text(e.data.end_point.val());
// 		});
// 		
// 	}
// 	
// 	function relate_to_form(event)
// 	{
// 		var e = event;
// 		var f = $('<div class="pop-form"></div>');
// 		var dp = $('<input class="big-input" type="text" />');
// 		var n = $('<textarea class="tiny-textarea" />');
// 		
// 		var s = $('<div class="button submit-rel">commit</>');
// 		
// 	}
	
	setInterval(load_docs, 20000);
	
	$('#new-key-submit').on('click', new_part);
	
	$('#submit-box').on('click', function(e){
		$('#root').submit();
	});
	
	$('#key-viewer-close').on('click', function(e){
		$('#key-viewer-box').hide('slide',{direction:'right'}, d_slider_speed, function(){
			$('#doclist-box').show('slide',{direction:'left'}, d_slider_speed);
		});
	});
	
	
	load_docs();
});
