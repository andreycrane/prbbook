plugin = ($) ->
	$.fn.toJSON = ->
		inputs = @serializeArray()
		object = {}
		$(inputs).each (index)->
			if @name? and @value?
				object[@name] = parseFloat(@value.replace(",", "."))
		return JSON.stringify(object)

plugin jQuery

$ ->
	$('#preview').click (event)->
		form = $('#edit_form')
		object = form.toJSON()
		problem = $("#first_image").attr("problem")
		stage_count = $("#first_image").attr("stages")
		first_img_url = "/problems/problem/#{problem}/img/#{object}/"
		second_img_url = "/problems/problem/#{problem}/img/#{object}/stage/#{stage_count}/"
		console.log object.b1, object, problem, first_img_url, second_img_url
		$.getJSON '/problems/problem/preview/', { problem: problem, in_params: object }, (data, textStatus, jqXHR)->
			console.log "Data: ", data
			console.log "textStatus: ", textStatus
			console.log "jqXHR: ", jqXHR

			if textStatus == "success"
				# если запрос завершился удачно
				# выясняем как прошел расчет по заданным параметрам
				if data.status == "success"
					# если удачно меняем изображения и расчитанное решение задачи
					$("#first_image").attr({'src': first_img_url })
					$("#second_image").attr({'src': second_img_url })
					# TODO: добавить смену решения
					$("#out_params").html(data.body)
				else if data.status == "error"
					$("#error-text").html(data.body)
					$('#error-modal').modal()
			else if textStatus == "error"
				# если запрос завершился с ошибкой
				alert("Error 500. Запрос к серверу завершился с ошибкой.")

	$('#save').click (event)->
		# глушим предопределенные действие отправки формы
		event.preventDefault()
		# собираем данные формы в JSON объект
		form = $('#edit_form')
		object = form.toJSON()
		# извлекаем id задания
		problem = $("#first_image").attr("problem")
		console.log object
		# выполняем запрос проверки исходных данных перед сохранением
		$.getJSON '/problems/problem/preview/', { problem: problem, in_params: object }, (data, textStatus, jqXHR)->
			console.log "Data: ", data
			console.log "textStatus: ", textStatus
			console.log "jqXHR: ", jqXHR

			if textStatus == "success"
				# если запрос завершился удачно
				# выясняем как прошел расчет по заданным параметрам
				if data.status == "success"
					$("#edit_form").submit()
				else if data.status == "error"
					# выводим модальное окно с сообщением об ошибке
					$("#save-error-text").html(data.body)
					$('#save-error-modal').modal()
			else if textStatus == "error"
				# если запрос завершился с ошибкой
				alert("Error 500. Запрос к серверу завершился с ошибкой.")
