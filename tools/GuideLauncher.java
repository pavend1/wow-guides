import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Starts Python guide scripts from IntelliJ IDEA (no Python plugin required).
 * Working directory must be the project root ($PROJECT_DIR$).
 */
public final class GuideLauncher {

    public static void main(String[] args) throws IOException, InterruptedException {
        Path root = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();
        String python = System.getenv().getOrDefault("PYTHON", "python");

        List<String> command = new ArrayList<>();
        command.add(python);

        if (args.length > 0 && "build".equalsIgnoreCase(args[0])) {
            command.add(root.resolve("scripts/build_guide_site.py").toString());
        } else {
            command.add(root.resolve("scripts/serve_guides.py").toString());
            command.add("--build");
            command.add("--open");
            command.add("--port");
            command.add("8080");
        }

        ProcessBuilder process = new ProcessBuilder(command);
        process.directory(root.toFile());
        process.inheritIO();

        int exitCode = process.start().waitFor();
        System.exit(exitCode);
    }
}
