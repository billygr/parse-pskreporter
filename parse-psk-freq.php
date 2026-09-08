<?php
// Parse https://www.pskreporter.info/cgi-bin/psk-freq.pl to my liking
// Converted from Python to PHP

header("Content-type: text/plain; charset=us-ascii\r\n");

// Load frequency to band mapping from external JSON file
function load_frequency_map($filename = 'frequency_map.json') {
    if (!file_exists($filename)) {
        fwrite(STDERR, "Error: Frequency mapping file '$filename' not found\n");
        exit(1);
    }

    $content = file_get_contents($filename);
    $map = json_decode($content, true);

    if ($map === null) {
        fwrite(STDERR, "Error: Invalid JSON format in '$filename'\n");
        exit(1);
    }

    return $map;
}

// Load the frequency mapping
$rep = load_frequency_map();

// Display script execution timestamp
echo "Script executed at: " . gmdate("Y-m-d H:i:s") . " UTC\r\n\r\n";

$data_file = 'psk-freq.pl';

if (!file_exists($data_file) || !is_readable($data_file)) {
    exit("Unable to open file $data_file");
}

// Last modified time
$dt = filemtime($data_file);
echo "Last Modified: " . gmdate("Y-m-d H:i:s", $dt) . " UTC\r\n";

// Read lines, skipping comments and lines starting with '0'
$lines = [];
$file_lines = file($data_file, FILE_IGNORE_NEW_LINES);
foreach ($file_lines as $line) {
    if (strpos($line, '#') === 0) {
        continue;
    }
    if (strpos($line, '0') === 0) {
        continue;
    }
    $lines[] = rtrim($line);
}

// Sort the frequency-to-band mapping by key length descending
// so longer/more specific frequency strings are replaced before shorter ones
$rep_keys = array_keys($rep);
usort($rep_keys, function($a, $b) {
    return strlen($b) - strlen($a);
});

// Convert freq to wavelength (band name) for each line
$psk_wavelength_list = [];
foreach ($lines as $line) {
    foreach ($rep_keys as $freq) {
        if (strpos($line, $freq) !== false) {
            $line = str_replace($freq, $rep[$freq], $line);
            break; // one substitution per line, matching original behaviour
        }
    }
    $psk_wavelength_list[] = $line;
}

// Sort with wavelength/band
sort($psk_wavelength_list);

//    0        1     2     3   4
// frequency score #spots #tx #rx
// grid KM%, 10 mins

$band_list = [];

$bands = ["160m", "80m", "60m", "40m", "30m", "20m", "17m", "15m",
          "12m", "10m", "6m", "4m", "2m", "23cm", "13cm"];

$score = [];
$spots = [];
foreach ($bands as $b) {
    $score[$b] = 0;
    $spots[$b] = 0;
}

foreach ($psk_wavelength_list as $wavelength) {
    $m = preg_split('/\s+/', trim($wavelength));

    if (isset($m[0]) && in_array($m[0], $bands) && isset($m[1]) && isset($m[2])) {
        $score[$m[0]] += (int)$m[1];
        $spots[$m[0]] += (int)$m[2];
        $band_list[] = $m[0];
    } else {
        // just in case more frequencies added
        echo "Additional frequencies to add: " . $wavelength . "\r\n";
    }
}

// Score displayed is the SUM of all scores provided for all frequencies in this band
echo "\r\n";
echo "Score displayed is the SUM of all scores provided for all frequencies in this band\r\n";

printf("160m score: %-5s spots: %s\r\n", $score["160m"], $spots["160m"]);
printf(" 80m score: %-5s spots: %s\r\n", $score["80m"], $spots["80m"]);
printf(" 60m score: %-5s spots: %s\r\n", $score["60m"], $spots["60m"]);
printf(" 40m score: %-5s spots: %s\r\n", $score["40m"], $spots["40m"]);
printf(" 30m score: %-5s spots: %s\r\n", $score["30m"], $spots["30m"]);
printf(" 20m score: %-5s spots: %s\r\n", $score["20m"], $spots["20m"]);
printf(" 17m score: %-5s spots: %s\r\n", $score["17m"], $spots["17m"]);
printf(" 15m score: %-5s spots: %s\r\n", $score["15m"], $spots["15m"]);
printf(" 12m score: %-5s spots: %s\r\n", $score["12m"], $spots["12m"]);
printf(" 10m score: %-5s spots: %s\r\n", $score["10m"], $spots["10m"]);
printf("  6m score: %-5s spots: %s\r\n", $score["6m"], $spots["6m"]);
printf("  4m score: %-5s spots: %s\r\n", $score["4m"], $spots["4m"]);
printf("  2m score: %-5s spots: %s\r\n", $score["2m"], $spots["2m"]);
printf("23cm score: %-5s spots: %s\r\n", $score["23cm"], $spots["23cm"]);
printf("13cm score: %-5s spots: %s\r\n", $score["13cm"], $spots["13cm"]);

echo "\r\n";
printf("160m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["160m"] ?? 0, $spots["160m"]);
printf(" 80m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["80m"] ?? 0, $spots["80m"]);
printf(" 60m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["60m"] ?? 0, $spots["60m"]);
printf(" 40m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["40m"] ?? 0, $spots["40m"]);
printf(" 30m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["30m"] ?? 0, $spots["30m"]);
printf(" 20m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["20m"] ?? 0, $spots["20m"]);
printf(" 17m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["17m"] ?? 0, $spots["17m"]);
printf(" 15m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["15m"] ?? 0, $spots["15m"]);
printf(" 12m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["12m"] ?? 0, $spots["12m"]);
printf(" 10m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["10m"] ?? 0, $spots["10m"]);
printf("  6m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["6m"] ?? 0, $spots["6m"]);
printf("  4m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["4m"] ?? 0, $spots["4m"]);
printf("  2m Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["2m"] ?? 0, $spots["2m"]);
printf("23cm Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["23cm"] ?? 0, $spots["23cm"]);
printf("13cm Frequencies: %-5s spots: %s\r\n", array_count_values($band_list)["13cm"] ?? 0, $spots["13cm"]);
