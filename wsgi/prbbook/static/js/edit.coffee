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
        engine = $("#edit_form").attr("engine")
        stage_count = $("#edit_form").attr("stages")
        first_img_url = "/problems/engines/#{engine}/img/#{object}/stage/1/"
        second_img_url = "/problems/engines/#{engine}/img/#{object}/stage/#{stage_count}/"
        console.log object, engine, stage_count, first_img_url, second_img_url

        $.getJSON '/problems/engines/preview/request', {engine: engine, in_params: object }, (data, textStatus, jqXHR)->
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