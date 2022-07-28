package com.example.ess;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

public class BranchesActivity extends AppCompatActivity {

    private ListView listView;
    private ArrayList<Branch> detailsArrayList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_branches);

        listView = findViewById(R.id.listView);

        showDetails();

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int i, long id) {

                String selected = String.valueOf(detailsArrayList.get(i).getId());

//                Intent intent = new Intent(BranchesActivity.this, BranchDetailsActivity.class);
//                intent.putExtra("id", selected);
//                startActivity(intent);

            }
        });

    }

    private void showDetails()
    {
        detailsArrayList.clear();
        listView.setAdapter(null);

        BranchAdapter branchAdapter = new BranchAdapter(this, R.layout.row_branches_item, detailsArrayList);
        listView.setAdapter(branchAdapter);

        detailsArrayList.add(new Branch("1", "Colombo"));
        detailsArrayList.add(new Branch("1", "Colombo Station"));
        detailsArrayList.add(new Branch("1", "Mirihana"));
        detailsArrayList.add(new Branch("1", "Maharagama"));
        detailsArrayList.add(new Branch("1", "Kottawa"));
        detailsArrayList.add(new Branch("1", "Nugegoda"));
        detailsArrayList.add(new Branch("1", "Kirilapana"));
        branchAdapter.notifyDataSetChanged();

    }

}

class Branch {

    String id, title;

    public Branch(String id, String title) {
        this.id = id;
        this.title = title;
    }

    public String getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }
}

class BranchAdapter extends ArrayAdapter<Branch> {

    private Context mContext;
    private int mResource;

    public BranchAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Branch> objects) {
        super(context, resource, objects);

        this.mContext = context;
        this.mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);
        convertView = layoutInflater.inflate(mResource, parent, false);

        TextView title = (TextView) convertView.findViewById(R.id.title);
        title.setText(getItem(position).getTitle());

        return convertView;
    }

}