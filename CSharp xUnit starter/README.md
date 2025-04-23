# C# 7 + xUnit Starter for Coding Dojo

This project provides a starter pack for Coding Dojo sessions using C# 7 and xUnit for testing. It is designed to help you quickly set up a C# project with xUnit as the testing framework so that you can focus on practicing coding katas and improving your programming skills.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- .NET Core SDK (compatible with C# 7)
- Your favorite IDE (e.g., Visual Studio, Visual Studio Code, JetBrains Rider)

## Getting Started

To get started with the C# 7 + xUnit starter, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/your-username/csharp-xunit-starter.git
cd csharp-xunit-starter
dotnet test # Or execute with the IDE
```
## Consigne Mars Rover

Vous faites partie de l'équipe qui explore Mars en envoyant un robot contrôlé à distance. Développez une API qui traduit les commandes envoyées depuis la terre en déplacement du robot.

### Exigences

- On considère que le terrain est un carré de 20x20.
- Le robot commence à un point précis (x, y), et dans une direction (Nord, Sud, Ouest, Est).
- Implémentez une commande pour avancer et reculer.
- Implémentez une commande de rotation.
- Prenez en compte les bordures (Les planètes sont des sphères ;-)).
- Implémentez une détection d'obstacle à chaque déplacement. Si un obstacle est présent, le déplacement s'arrête au dernier point possible.
- Implémenter une gestion du déplacement à 45°