# EazyClip-Video-Maker
<p>Making videos easily from images.</p>
<p>The will behind this project is to turn easy to create a video from a sequence of images. In fact, this is already not hard, but I saw it would be easier as it's a few ways work.</p>
<h3>Using it</h3>
<p> By now the using flow follows the below:</p>
<ul>
    <li>Create a folder with (and only with) all the files you want in your videoclip;</li>
    <li>Run run.py to open EazyClip;</li>
    <li>Click on "Selecionar" (select) to open the selecting folder window, and select your project folder;</li>
    <li>If you don't want a audio track in your clip, uncheck the checkbox "Audio";</li>
    <li>Select your duration defining method. It can be:
        <ul>
            <li><b>"Definir duração total" (define total duration)</b>: set the total duration of the video, and all the images on it will have the same duration (total duration divided by the number of images);</li>
            <li><b>"Definir duração por imagem" (define duration by image)</b>: set the duration of each image, then all the images on the videoclip will have the same duration (as you setted), and the video will have the total duration as image duration times the number of images;</li>
            <li><b>"Ajustar ao áudio" (Fit on audio)</b>: the video will have the same duration of the audio, which will be divided by each image (just like "define total duration").</li>
        </ul>
    </li>
    <li>Click "Gerar video" (generate video) to start the process. By now the window is getting freezed the building time along, but it comes back when the rendering is over.</li>
</ul>
<h3>Future Features</h3>
<p>This is just a MVP, and with this point of the project I've already achieved my first goal turning my work easy. By now these are the features I want to add:</p>
<ul>
    <li><b>Executable file</b>: Turn the platform into a executable program;</li>
    <li><b>Each image duration set</b>: Allow the user to set each image duration seeing a miniature of it on the window.</li>
    <li><b>Notifications</b>: Send a alert when the video is done. It will be:
        <ul>
            <li>Sound alert;</li>
            <li>Telegram message;</li>
            <li>E-mail.</li>
        </lu>
    </li>
</ul>
