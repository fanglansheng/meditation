document.addEventListener('DOMContentLoaded', function() {

  var addSoundButton = document.getElementById('addToSound');
  addSoundButton.addEventListener('click', function() {

    chrome.tabs.getSelected(null, function(tab) {

      var soundName = document.getElementById('soundName').value;

      d = document;
      var f = d.createElement('form');
      f.action = 'http://localhost:8000/meditation/create-sound-plugin';
      f.method = 'post';

      var i1 = d.createElement('input');
      i1.type = 'hidden';
      i1.name = 'name';
      i1.value = soundName;
      f.appendChild(i1);

      var i2 = d.createElement('input');
      i2.type = 'hidden';
      i2.name = 'url';
      i2.value = tab.url;
      f.appendChild(i2);

      d.body.appendChild(f);
      f.submit();
    });
  }, false);

  var addMusicButton = document.getElementById('addToMusic');
  addMusicButton.addEventListener('click', function() {

    chrome.tabs.getSelected(null, function(tab) {
      var musicName = document.getElementById('musicName').value;

      d = document;
      var f = d.createElement('form');
      f.action = 'http://localhost:8000/meditation/create-music-plugin';
      f.method = 'post';

      var i1 = d.createElement('input');
      i1.type = 'hidden';
      i1.name = 'name';
      i1.value = musicName;
      f.appendChild(i1);

      var i2 = d.createElement('input');
      i2.type = 'hidden';
      i2.name = 'url';
      i2.value = tab.url;
      f.appendChild(i2);

      d.body.appendChild(f);
      f.submit();
    });
  }, false);
}, false);
