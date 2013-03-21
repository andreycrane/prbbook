class Transliterator
    @translit_map:
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g','д': 'd', 'е': 'e', 'ё': 'jo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',  'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shh', 'ъ':'#', 'ы': 'y', 'ь': '\'', 'э': 'je',
        'ю': 'ju', 'я': 'ja', ' ': '_', '.': '.'

    @transliterate: (word)->
        word = word.toLowerCase()
        translit = ""
        for ch in word
            cymbol = @translit_map[ch]
            translit += if cymbol? then cymbol else ch
        return translit

$ ->
    $('#id_name').bind 'input', (event)->
        if $('#translitCheckbox').is(':checked')
            first_name = $('#id_name').val()
            translit = Transliterator.transliterate(first_name)
            $('#id_login').val(translit)
            $('#id_password').val(translit)
            $('#id_retype').val(translit)

    $('#translitCheckbox').click ->
        $('#id_name').trigger('input')