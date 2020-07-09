# File Upload

## Notes

* Null bytes, e.g. .php%00.jpg, where .jpg gets truncated and .php becomes the new extension

* Try to upload a file with a double extension (ex: file.png.php or file.png.php5).

* PHP extensions: .php, .php2, .php3, .php4, .php5, .php6, .php7, .phps, .pht, .phtml, .pgif, .shtml, .htaccess, .phar, .inc
ASP extensions: .asp, .aspx, .config

* Try to uppercase some letter(s) of the extension. Like: .pHp, .pHP5, .PhAr ...

* Try to upload some reverse double extension (useful to exploit Apache misconfigurations where anything with extension .php, but not necessarily ending in .php will execute code):
ex: file.php.png

* Bypass Content-Type checks by setting the value of the Content-Type header to: image/png , text/plain , application/octet-stream

* Bypass magic number check by adding at the beginning of the file the bytes of a real image (confuse the file command).  (".PNG....", "GIF89a" ,)