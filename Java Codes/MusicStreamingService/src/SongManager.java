import java.util.ArrayList;
import java.util.List;

public class SongManager {

    private Song currentSong;

    public void play(Song song) {
        this.currentSong = song;
        System.out.println("Playing: " + song.getSongName());
    }

    public void pause() {
        if (currentSong != null) {
            System.out.println("Paused: " + currentSong.getSongName());
        } else {
            System.out.println("No song is currently playing.");
        }
    }

    public void skip() {
        if (currentSong != null) {
            System.out.println("Skipping: " + currentSong.getSongName());
            currentSong = null; // Resetting current song as an example
        } else {
            System.out.println("No song is currently playing.");
        }
    }
}
