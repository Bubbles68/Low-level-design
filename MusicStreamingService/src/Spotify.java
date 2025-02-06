import java.util.ArrayList;
import java.util.List;

public class Spotify {
    public static void main(String[] args) {
        // Creating users and songs
        User user1 = new User("Kavya");
        Song song1 = new Song("Shape of You", "Ed Sheeran", 230);
        Song song2 = new Song("Blinding Lights", "The Weeknd", 200);

        // Adding songs to a playlist
        Playlist playlist1 = user1.createPlaylist("Favorites");
        playlist1.addSong(song1);
        playlist1.addSong(song2);

        // Creating a player
        SongManager player = new SongManager();
        player.play(song1);
        player.pause();
        player.skip();

        // Searching for a song
        List<Song> library = new ArrayList<>();
        library.add(song1);
        library.add(song2);
        user1.searchSong("Shape", library);
    }
}