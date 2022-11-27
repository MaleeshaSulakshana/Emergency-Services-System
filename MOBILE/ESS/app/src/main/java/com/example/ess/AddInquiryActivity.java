package com.example.ess;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.ess.Classes.API;
import com.example.ess.Classes.Preferences;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.Console;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;

public class AddInquiryActivity extends AppCompatActivity implements LocationListener {

    private Button btnAdd, btnSelectImages, btnSelectVideo;
    private EditText details, location, contact;
    private TextView imageCount, videoCount;
    private ProgressBar progressBar;

    private String id = "";

    private static final int PICK_IMAGE = 100;
    private static final int REQUEST_TAKE_GALLERY_VIDEO = 3;
    private Uri imageUri = Uri.EMPTY;
    private ArrayList<Bitmap> bitmapList = new ArrayList<Bitmap>();
    private String videoPath = "", lat = "", lon = "" ;

    private LocationManager locationManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_inquiry);

        Intent intentThis = getIntent();
        id = intentThis.getStringExtra("id");

        btnAdd = (Button) this.findViewById(R.id.btnAdd);
        progressBar = (ProgressBar) this.findViewById(R.id.progressBar);
        btnSelectImages = (Button) this.findViewById(R.id.btnSelectImages);
        btnSelectVideo = (Button) this.findViewById(R.id.btnSelectVideo);

        details = (EditText) this.findViewById(R.id.details);
        location = (EditText) this.findViewById(R.id.location);
        contact = (EditText) this.findViewById(R.id.contact);

        imageCount = (TextView) this.findViewById(R.id.imageCount);
        videoCount = (TextView) this.findViewById(R.id.videoCount);

//        Get user permission for gps
        try {
            if (ContextCompat.checkSelfPermission(getApplicationContext(), android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED ) {
                ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION}, 101);
            }
        } catch (Exception e){
            e.printStackTrace();
        }

        try {
            if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED ) {
                ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.READ_EXTERNAL_STORAGE}, 102);
            }
        } catch (Exception e){
            e.printStackTrace();
        }

        try {
            locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, this);
            Location currentLocation = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);

            if (currentLocation != null) {

                double latitude = currentLocation.getLatitude();
                double longitude = currentLocation.getLongitude();

                lat = String.valueOf(latitude);
                lon = String.valueOf(longitude);

            }


        }
        catch(SecurityException e) {
            e.printStackTrace();
        }

        btnSelectImages.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                openGalleryForSelectImages();

            }
        });

        btnSelectVideo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                openGalleryForSelectVideo();

            }
        });

        btnAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if (lat != "" && lon != "") {

                    Toast.makeText(AddInquiryActivity.this, "Please wait for upload your inquiry. It take few minutes!",Toast.LENGTH_SHORT).show();
                    progressBar.setVisibility(View.VISIBLE);
                    btnAdd.setEnabled(false);

                    String strDetails = details.getText().toString();
                    String strLocation = location.getText().toString();
                    String strContact = contact.getText().toString();

                    if (strDetails.equals("") || strContact.equals("") || strLocation.equals("")) {
                        btnAdd.setEnabled(true);
                        progressBar.setVisibility(View.VISIBLE);
                        Toast.makeText(AddInquiryActivity.this, "Fields are empty!",Toast.LENGTH_SHORT).show();

                    } else if (strContact.length() != 10) {
                        btnAdd.setEnabled(true);
                        progressBar.setVisibility(View.VISIBLE);
                        Toast.makeText(AddInquiryActivity.this, "Please check your mobile number!",Toast.LENGTH_SHORT).show();

                    } else if (bitmapList.size() == 0) {
                        btnAdd.setEnabled(true);
                        progressBar.setVisibility(View.VISIBLE);
                        Toast.makeText(AddInquiryActivity.this, "Please add one or more images for proof!",Toast.LENGTH_SHORT).show();

                    } else {

                        try {
                            String URL = API.INQUIRIES_API + "/add_inquiry";

                            JSONArray jsonArray = new JSONArray();
                            for (int i=0; i < bitmapList.size(); i++) {
                                JSONObject jsonBody = new JSONObject();
                                String image = getStringImage(bitmapList.get(i));
                                jsonBody.put("image", image);
                                jsonArray.put(jsonBody);
                            }

                            JSONObject parameter =  new JSONObject();
                            parameter.put("images", jsonArray);
                            parameter.put("details", strDetails);
                            parameter.put("location", strLocation);
                            parameter.put("contact", strContact);
                            parameter.put("user_id", Preferences.LOGGED_USER_ID);
                            parameter.put("branch", id);
                            parameter.put("lat", lat);
                            parameter.put("lon", lon);

                        if (!videoPath.equals("")) {
                            File file = new File(videoPath);

                            String vdo = videoToBase64(file);
                            parameter.put("video", vdo);

                        }

                            JsonObjectRequest jsonObject = new JsonObjectRequest(Request.Method.POST, URL, parameter, new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {

                                    try {

                                        String status = response.getString("status");
                                        String msg = response.getString("msg");

                                        Toast.makeText(AddInquiryActivity.this, msg, Toast.LENGTH_SHORT).show();

                                        if (status.equals("success")) {
                                            Intent intent = new Intent(AddInquiryActivity.this, InquiriesActivity.class);
                                            startActivity(intent);
                                            finish();
                                        } else {
                                            btnAdd.setEnabled(true);
                                            progressBar.setVisibility(View.VISIBLE);
                                        }

                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }

                                }
                            }, new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    Toast.makeText(AddInquiryActivity.this, error.getMessage().toString(), Toast.LENGTH_SHORT).show();
                                }
                            });

                            RequestQueue queue = Volley.newRequestQueue(AddInquiryActivity.this);
                            queue.add(jsonObject);

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }

                } else {
                    Toast.makeText(AddInquiryActivity.this, "Waiting for get your location.", Toast.LENGTH_SHORT).show();
                }

            }
        });

    }

    private String videoToBase64(File file) {
        String encodedString = null;

        InputStream inputStream = null;
        try {
            inputStream = new FileInputStream(file);
        } catch (Exception e) {
        }
        byte[] bytes;
        byte[] buffer = new byte[8192];
        int bytesRead;
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        try {
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                output.write(buffer, 0, bytesRead);
            }
        } catch (IOException e) {

        }
        bytes = output.toByteArray();
        encodedString = Base64.encodeToString(bytes, Base64.DEFAULT);

        return encodedString;
    }

    private void openGalleryForSelectVideo()
    {
        Intent intent = new Intent();
        intent.setType("video/*");
        intent.putExtra(Intent.ACTION_PICK, true);
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent,"Select Video"), REQUEST_TAKE_GALLERY_VIDEO);
    }

    private void openGalleryForSelectImages()
    {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent,"Select Images"), PICK_IMAGE);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK) {
            if (requestCode == PICK_IMAGE) {
                if (data.getClipData() != null) {
                    bitmapList = new ArrayList<Bitmap>();
                    int count = data.getClipData().getItemCount();
                    for (int i = 0; i < count; i++) {
                        try {
                            Uri imageUri = data.getClipData().getItemAt(i).getUri();
                            Bitmap bitmap = (Bitmap) MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
                            bitmapList.add(bitmap);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    imageCount.setText(String.valueOf(bitmapList.size()) + " Images selected");
                }
                
            } else {

                Uri videoUri = data.getData();
                String selectedVideoPAth = getPath(videoUri);
                if (selectedVideoPAth != null) {
                    videoPath = selectedVideoPAth;
                    videoCount.setText("1 Video selected");
                }

            }
        }
    }

    public String getPath(Uri uri) {
        String[] projection = { MediaStore.Video.Media.DATA };
        Cursor cursor = getContentResolver().query(uri, projection, null, null, null);
        if (cursor != null) {
            int column_index = cursor
                    .getColumnIndexOrThrow(MediaStore.Video.Media.DATA);
            cursor.moveToFirst();
            return cursor.getString(column_index);
        } else
            return null;
    }

    public String getStringImage(Bitmap bmp) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
        byte[] imageBytes = byteArrayOutputStream.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;
    }

    @Override
    public void onLocationChanged(@NonNull Location location) {

    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {
    }

    @Override
    public void onProviderEnabled(@NonNull String provider) {
    }

    @Override
    public void onProviderDisabled(String provider) {
        Toast.makeText(AddInquiryActivity.this, "Please Enable GPS and Internet", Toast.LENGTH_SHORT).show();
    }

}