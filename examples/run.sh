#!/bin/bash

for file in info_M*_wafer_globalChannelId_readoutSequence.png; do
  # Extract the wafer type from the filename
  wafer_type=$(echo $file | sed 's/info_\(M[HL]_[A-Z0-9]\)_wafer_globalChannelId_readoutSequence.png/\1/')

  # Create the new filename
  new_name="${wafer_type}_wafer_example.png"

  # Rename
  mv "$file" "$new_name"

  echo "Renamed $file to $new_name"
done

echo "All files renamed and copied to examples directory."
