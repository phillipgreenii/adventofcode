

start-shell() {
    profileName="${1}"  

    if [[ "$#" -ne 1 ]]; then
        echo "profileName is required" >&2
        exit 1
    fi  

    PROFILES_PATH=~/.nix-profiles
    mkdir -p "${PROFILES_PATH}"

    profilePath="${PROFILES_PATH}/${profileName}"

    if [[ -f "${profilePath}" ]]; then
    nix develop "${profilePath}"
    else
    nix develop --profile "${profilePath}"
    fi
}
