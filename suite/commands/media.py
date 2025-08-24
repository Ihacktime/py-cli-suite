import click
from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable
from tqdm import tqdm
import os

class YouTubeDownloader:
    def __init__(self, url, quality="highest", output_path="."):
        self.url = url
        self.quality = quality
        self.output_path = output_path
        self.yt = YouTube(
            url,
            on_progress_callback=self.on_progress,
            on_complete_callback=self.on_complete,
        )
        self.pbar = None

    def download(self):
        try:
            # If user wants the highest resolution, use 'get_highest_resolution' filter
            if self.quality == "highest":
                video_stream = self.yt.streams.filter(
                    progressive=True, file_extension="mp4"
                ).get_highest_resolution()
            else:
                video_stream = self.yt.streams.filter(
                    progressive=True, res=self.quality, file_extension="mp4"
                ).first()

            if video_stream is None:
                available_qualities = [
                    str(stream.resolution)
                    for stream in self.yt.streams.filter(
                        progressive=True, file_extension="mp4"
                    )
                ]
                click.echo(f"No streams found with the specified quality: {self.quality}")
                click.echo(f"Title: {self.yt.title}")
                click.echo(f"Available qualities: {available_qualities}")
                return False

            # Initialize tqdm progress bar
            self.pbar = tqdm(
                total=video_stream.filesize,
                unit="B",
                unit_scale=True,
                desc=self.yt.title,
            )

            # Download the video
            video_stream.download(self.output_path)
            return True

        except VideoUnavailable as e:
            click.echo(f"An error occurred: {e}")
            if self.pbar:
                self.pbar.close()  # Ensure the progress bar is closed in case of error
            return False

    def on_progress(self, stream, chunk, bytes_remaining):
        """
        Updates the progress bar during the download.

        :param stream: Stream being downloaded.
        :param chunk: Chunk of data being downloaded.
        :param bytes_remaining: Number of bytes remaining to be downloaded.
        """
        current = stream.filesize - bytes_remaining
        self.pbar.update(current - self.pbar.n)  # update pbar with the downloaded bytes

    def on_complete(self, stream, file_path):
        """
        Completes the progress bar and prints the download completion message.

        :param stream: Stream that has been downloaded.
        :param file_path: The file path of the downloaded video.
        """
        self.pbar.close()
        click.echo(f"\nDownloaded '{self.yt.title}' successfully to: {file_path}")

@click.group()
def media():
    """Media tools: YouTube downloader, etc."""
    pass

@media.command()
@click.argument('url')
@click.option('--quality', '-q', default='highest', 
              help='Video quality (e.g., 720p, 1080p, highest)')
@click.option('--output-path', '-o', default='.', 
              help='Output directory for downloaded files')
def youtube(url, quality, output_path):
    """Download YouTube videos."""
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    downloader = YouTubeDownloader(url, quality, output_path)
    success = downloader.download()
    
    if not success:
        click.echo("Download failed.")