// Generated by CoffeeScript 1.4.0
(function() {
  var Transliterator;

  Transliterator = (function() {

    function Transliterator() {}

    Transliterator.translit_map = {
      'а': 'a',
      'б': 'b',
      'в': 'v',
      'г': 'g',
      'д': 'd',
      'е': 'e',
      'ё': 'jo',
      'ж': 'zh',
      'з': 'z',
      'и': 'i',
      'й': 'j',
      'к': 'k',
      'л': 'l',
      'м': 'm',
      'н': 'n',
      'о': 'o',
      'п': 'p',
      'р': 'r',
      'с': 's',
      'т': 't',
      'у': 'u',
      'ф': 'f',
      'х': 'h',
      'ц': 'c',
      'ч': 'ch',
      'ш': 'sh',
      'щ': 'shh',
      'ъ': '#',
      'ы': 'y',
      'ь': '\'',
      'э': 'je',
      'ю': 'ju',
      'я': 'ja',
      ' ': '_',
      '.': '.'
    };

    Transliterator.transliterate = function(word) {
      var ch, cymbol, translit, _i, _len;
      word = word.toLowerCase();
      translit = "";
      for (_i = 0, _len = word.length; _i < _len; _i++) {
        ch = word[_i];
        cymbol = this.translit_map[ch];
        translit += cymbol != null ? cymbol : ch;
      }
      return translit;
    };

    return Transliterator;

  })();

  $(function() {
    $('#id_name').bind('input', function(event) {
      var first_name, translit;
      if ($('#translitCheckbox').is(':checked')) {
        first_name = $('#id_name').val();
        translit = Transliterator.transliterate(first_name);
        $('#id_login').val(translit);
        $('#id_password').val(translit);
        return $('#id_retype').val(translit);
      }
    });
    return $('#translitCheckbox').click(function() {
      return $('#id_name').trigger('input');
    });
  });

}).call(this);
