/*
 * day_18.cpp
 *
 *  Created on: 20 déc. 2019
 *      Author: Florent
 */

#include <cstdlib>
#include <cstdio>
#include <cctype>

#include <utility>
#include <string>
#include <map>
#include <set>
#include <vector>
#include <fstream>

#include <chrono>

typedef std::pair<int, int> Point;

// directions et point suivant selon une direction
enum Direction {
    Up, Down, Left, Right
};
static inline Point direction_next(Direction d, const Point &p) {
    switch (d) {
    case Up:
        return Point(p.first, p.second - 1);
    case Down:
        return Point(p.first, p.second + 1);
    case Left:
        return Point(p.first - 1, p.second);
    case Right:
        return Point(p.first + 1, p.second);
    }
    return Point(0, 0);
}

class World {
public:
    typedef std::pair<int, std::set<char> > Path; // distance, liste des portes rencontrées
    typedef std::map<char, Path> Paths; // pour chaque point d'intérêt, la liste des chemins vers les autres points d'intérêts

    std::map<Point, char> m_world; // tout le plateau
    std::map<char, Point> m_start_positions; // la ou les (partie 2) positions de départ
    std::map<char, Point> m_keys; // les clés
    std::map<char, Point> m_doors; // les portes
    std::map<char, Paths> m_paths; // tous les chemins qu'on est susceptible de faire avec leurs distances
    std::map<std::string, int> m_rec_cache; // un cache pour les appels à rec_search

    World(const std::string &lines, bool part_2 = false) :
            m_world(), m_start_positions(), m_keys(), m_doors(), m_paths(), m_rec_cache() {
        // parse
        int x = 0;
        int y = 0;
        for (const char c : lines) {
            if (c == '\n') {
                x = 0;
                y += 1;
                continue;
            }
            m_world[Point(x, y)] = c;
            if (c == '@') {
                m_start_positions['@'] = Point(x, y);
            } else if (islower(c)) {
                m_keys[c] = Point(x, y);
            } else if (isupper(c)) {
                m_doors[c] = Point(x, y);
            }
            x += 1;
        }

        // ajustements pour la partie 2, la zone de départ est modifiée et on a 4 robots
        // les points de départ des robots seront @ = $ &
        if (part_2) {
            Point start_pos = m_start_positions['@'];
            m_start_positions['@'] = Point(start_pos.first + 1, start_pos.second + 1);
            m_start_positions['='] = Point(start_pos.first + 1, start_pos.second - 1);
            m_start_positions['$'] = Point(start_pos.first - 1, start_pos.second + 1);
            m_start_positions['&'] = Point(start_pos.first - 1, start_pos.second - 1);
            m_world[m_start_positions['@']] = '@';
            m_world[m_start_positions['=']] = '=';
            m_world[m_start_positions['$']] = '$';
            m_world[m_start_positions['&']] = '&';

            m_world[start_pos] = '#';
            m_world[Point(start_pos.first + 1, start_pos.second + 0)] = '#';
            m_world[Point(start_pos.first - 1, start_pos.second + 0)] = '#';
            m_world[Point(start_pos.first + 0, start_pos.second + 1)] = '#';
            m_world[Point(start_pos.first + 0, start_pos.second - 1)] = '#';
        }

        // précalculer les chemins entre les positions de départ et les clés
        // ainsi qu'entre les différentes clés
        // on stocke la distance et les portes rencontrées (en minuscules)
        for (const auto &s : m_start_positions) {
            m_paths[s.first] = cache_paths(s.second);
        }
        for (const auto &s : m_keys) {
            m_paths[s.first] = cache_paths(s.second);
        }
    }

    int work() {
        // un set avec le ou les points de départ
        std::set<char> start_points;
        for (const auto &p : m_start_positions) {
            start_points.insert(p.first);
        }
        // un set avec toutes les clés à récupérer
        std::set<char> missing_keys;
        for (const auto &p : m_keys) {
            missing_keys.insert(p.first);
        }
        return rec_search(start_points, missing_keys);
    }

private:
    // calcul les chemins vers les autres clés à partir de la position donnée
    Paths cache_paths(const Point &position) {
        // un état pour la recherche
        struct State {
            Point m_position; // position du robot
            std::set<char> m_dependencies; // liste des portes déjà rencontrées

            State(const Point &p, const std::set<char> &d) :
                    m_position(p), m_dependencies(d) {
            }
        };
        constexpr Direction all_dirs[] = { Up, Down, Left, Right };

        std::vector<State> queue; // liste de positions à étudier
        queue.emplace_back(position, std::set<char>());
        std::map<Point, int> visited; // meilleures visites (point, distante)

        Paths paths; // retour

        int distance = 1;

        while (!queue.empty()) {
            decltype(queue) next_queue;
            for (const auto &s : queue) {
                for (const Direction d : all_dirs) {
                    Point next_p = direction_next(d, s.m_position);

                    // a-t-on déjà fait mieux
                    const auto &visited_next_p = visited.find(next_p);
                    if (visited_next_p != visited.end() && visited_next_p->second < distance) {
                        continue;
                    }

                    char v = m_world[next_p];
                    if (v == '#') { // mur
                        continue;
                    }

                    // une clé
                    if (islower(v)) {
                        paths[v] = Path(distance, s.m_dependencies);
                    }

                    // la suite du parcours
                    next_queue.emplace_back(next_p, s.m_dependencies);
                    State &next_s = next_queue.back();

                    // est-ceune porte, si oui mise à jour des dépendances
                    if (isupper(v)) {
                        next_s.m_dependencies.insert(tolower(v));
                    }

                    // enregistrer le passage
                    visited[next_p] = distance;
                }
            }
            queue = next_queue;
            distance += 1;
        }

        return paths;
    }

    int rec_search(const std::set<char> &points_names, const std::set<char> &missing_keys) {
        int best = -1;

        if (missing_keys.size() == 0) {
            return 0;
        }

        // la clé pour le cache d'appel sur rec_search
        // chaîne formée à partir des arguments
        std::string cache_key;
        cache_key.reserve(points_names.size() + missing_keys.size());
        for (char c : points_names) {
            cache_key.push_back(c);
        }
        for (char c : missing_keys) {
            cache_key.push_back(c);
        }
        const auto &cache_test = m_rec_cache.find(cache_key);
        if (cache_test != m_rec_cache.end()) {
            return cache_test->second;
        }

        for (char k : missing_keys) {
            // trouver qui peut chopper la clé k
            for (char bot : points_names) {
                // est-ce que ce bot l'a dans ses chemins possibles
                const auto &path_bot = m_paths[bot];
                const auto &path_search = path_bot.find(k);
                if (path_search == path_bot.end()) {
                    continue;
                }

                // on y va
                const Path &p = path_search->second;
                if (best != -1 and best <= p.first) {
                    // bon c'est pas un champion
                    continue;
                }

                // est-ce qu'on a toutes les clés pour ce chemin
                bool got_all_keys = true;
                for (char missing_key : missing_keys) {
                    if (p.second.count(missing_key)) {
                        got_all_keys = false;
                        break;
                    }
                }
                if (!got_all_keys) {
                    continue;
                }

                // continuer en mettant à jour la position de ce robot
                // et en retirant la clé des clés manquants
                std::set<char> new_search_points = points_names;
                new_search_points.erase(bot);
                new_search_points.insert(k);
                std::set<char> new_missing_keys = missing_keys;
                new_missing_keys.erase(k);
                int r = rec_search(new_search_points, new_missing_keys);
                // progrès ou non ?
                if (best == -1 || (r != -1 && best > p.first + r)) {
                    best = p.first + r;
                }
            }
        }

        m_rec_cache[cache_key] = best;
        return best;
    }

};

int main(int argc, char **argv) {
    const char *opt_filename = "input_18";
    if (argc == 2) {
        opt_filename = argv[1];
    }

    std::string input;
    std::ifstream file(opt_filename);
    if (!file.is_open()) {
        return 1;
    }
    file.seekg(0, std::ios::end);
    input.reserve(file.tellg());
    file.seekg(0, std::ios::beg);

    input.assign((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());

    auto start_p1 = std::chrono::high_resolution_clock::now();
    World world(input, false);
    int r_p1 = world.work();
    auto end_p1 = std::chrono::high_resolution_clock::now();

    printf("part1: %d (%f ms)\n", r_p1, std::chrono::duration<double, std::milli>(end_p1 - start_p1).count());
    printf("taille cache : %zu\n", world.m_rec_cache.size());

    auto start_p2 = std::chrono::high_resolution_clock::now();
    world = World(input, true);
    int r_p2 = world.work();
    auto end_p2 = std::chrono::high_resolution_clock::now();

    printf("part2: %d (%f ms)\n", r_p2, std::chrono::duration<double, std::milli>(end_p2 - start_p2).count());
    printf("taille cache : %zu\n", world.m_rec_cache.size());
}
