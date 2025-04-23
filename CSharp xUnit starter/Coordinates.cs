using System; // Ajout pour ArgumentOutOfRangeException et Console

namespace CSharp_xUnit_starter;

// Assurez-vous que l'enum Direction est défini quelque part accessible
// Si ce n'est pas le cas, vous pouvez l'ajouter ici ou dans son propre fichier.
public enum Direction { North, East, South, West }

public record Coordinates(int X, int Y, Direction Direction)
{
    // Méthodes existantes pour le déplacement
    public Coordinates YTranslate() => this with { Y = TranslateAroundTheWorld(Y) };
    public Coordinates YAntiTranslate() => this with { Y = AntiTranslateAroundTheWorld(Y) };
    public Coordinates XAntiTranslate() => this with { X = AntiTranslateAroundTheWorld(X) };
    public Coordinates XTranslate() => this with { X = TranslateAroundTheWorld(X) };

    // Méthode existante pour la rotation (semble anti-horaire)
    public Coordinates Rotate() => this with
    {
        Direction = Direction switch
        {
            Direction.North => Direction.West,
            Direction.East => Direction.North,
            Direction.South => Direction.East,
            Direction.West => Direction.South,
            _ => throw new ArgumentOutOfRangeException(nameof(Direction), Direction, "Invalid direction for Rotate")
        }
    };

    // Méthode existante pour la rotation inverse (semble horaire)
    public Coordinates AntiRotate() => this with
    {
        Direction = Direction switch
        {
            Direction.North => Direction.East,
            Direction.East => Direction.South,
            Direction.South => Direction.West,
            Direction.West => Direction.North,
            _ => throw new ArgumentOutOfRangeException(nameof(Direction), Direction, "Invalid direction for AntiRotate")
        }
    };

    // Méthodes d'aide existantes pour le passage aux bords du monde
    private int TranslateAroundTheWorld(int axis)
    {
        // Logique spécifique de votre code : passage de 20 à 0
        if (axis == 20)
            return 0;
        return axis + 1;
    }

    private int AntiTranslateAroundTheWorld(int axis)
    {
        // Logique spécifique de votre code : passage de 0 à 20
        if (axis == 0)
            return 20;
        return axis - 1;
    }

    // --- AJOUT POUR LA DÉPENDANCE CIRCULAIRE ---
    // Cette méthode crée une dépendance de Coordinates vers Rover,
    // car elle a besoin de connaître la définition de la classe Rover.
    public void LogPositionWithRoverInfo(Rover associatedRover)
    {
        // Vérifie que le rover n'est pas null pour éviter NullReferenceException
        if (associatedRover == null)
        {
            Console.WriteLine($"Coordinates ({X},{Y},{Direction}) - No associated rover provided.");
            return;
        }
        // Utilise une propriété ou méthode de l'objet Rover passé en paramètre.
        // Ici, on utilise simplement GetHashCode() comme exemple.
        Console.WriteLine($"Coordinates ({X},{Y},{Direction}) are associated with Rover instance: {associatedRover.GetHashCode()}");
        // Vous pourriez avoir une logique plus complexe ici qui utilise l'état du Rover.
        // Exemple : if (associatedRover.HasObstacleDetected) { ... }
    }
    // --- FIN DE L'AJOUT ---
}

// Assurez-vous que la classe Rover est définie dans le même namespace
// ou qu'un 'using' approprié est présent si elle est dans un autre namespace.
// Exemple minimal de la classe Rover pour que Coordinates compile :
/*
namespace CSharp_xUnit_starter
{
    public class Rover
    {
        public Coordinates Coordinates { get; }
        // public bool HasObstacleDetected { get; private set; } // Exemple de propriété utilisable

        public Rover(Coordinates coordinates)
        {
            Coordinates = coordinates;
        }
        // ... autres méthodes et propriétés ...
    }
}
*/